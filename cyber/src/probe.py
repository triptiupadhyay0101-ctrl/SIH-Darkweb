from __future__ import annotations

import hashlib
import json
import re
import socket
import ssl
import time
from datetime import datetime, timezone
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .classify import classify
from .config import is_valid_onion_v3, settings
from .correlate import build_infrastructure_linking_clue
from .db import connect
from .wallet_correlate import correlate_wallet
from .wallet_extract import extract_wallets


TITLE_RE = re.compile(
    r"<title[^>]*>(.*?)</title>",
    re.I | re.S,
)

DEFAULT_PAGE_PATTERNS = (
    "Apache2 Debian Default Page",
    "Apache2 Ubuntu Default Page",
    "Welcome to nginx!",
    "Test Page for the Nginx HTTP Server",
    "IIS Windows Server",
)

EXPOSED_PATH_CHECKS = {
    "/server-status": {
        "type": "EXPOSED_SERVER_STATUS",
        "severity": "high",
        "match": ("Apache", "server-status"),
    },
    "/server-info": {
        "type": "EXPOSED_SERVER_INFO",
        "severity": "high",
        "match": (
            "Server Information",
            "Apache Server Information",
        ),
    },
    "/.git/config": {
        "type": "EXPOSED_GIT_CONFIG",
        "severity": "critical",
        "match": (
            "[core]",
            "repositoryformatversion",
        ),
    },
    "/.env": {
        "type": "EXPOSED_ENV_FILE",
        "severity": "critical",
        "match": (
            "DB_",
            "APP_",
            "SECRET",
            "API_KEY",
        ),
    },
    "/phpinfo.php": {
        "type": "EXPOSED_PHPINFO",
        "severity": "high",
        "match": (
            "phpinfo()",
            "PHP Version",
        ),
    },
    "/phpmyadmin/": {
        "type": "EXPOSED_PHPMYADMIN",
        "severity": "medium",
        "match": ("phpMyAdmin",),
    },
    "/.htaccess": {
        "type": "EXPOSED_HTACCESS",
        "severity": "medium",
        "match": (
            "RewriteEngine",
            "Require",
            "Order ",
        ),
    },
    "/backup.zip": {
        "type": "EXPOSED_BACKUP_FILE",
        "severity": "high",
        "match": None,
    },
    "/wp-admin/install.php": {
        "type": "EXPOSED_WP_INSTALL",
        "severity": "high",
        "match": ("WordPress",),
    },
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_bounded_body(
    resp: requests.Response,
) -> bytes:
    """Read at most the configured response-body limit."""
    chunks: list[bytes] = []
    remaining = settings.max_body_bytes

    try:
        for chunk in resp.iter_content(chunk_size=8192):
            if not chunk:
                continue

            if len(chunk) >= remaining:
                chunks.append(chunk[:remaining])
                break

            chunks.append(chunk)
            remaining -= len(chunk)

            if remaining <= 0:
                break

    except requests.RequestException:
        return b""

    return b"".join(chunks)


def _decode_body(
    body: bytes,
    resp: requests.Response,
) -> str:
    """Decode bounded response bytes without loading resp.text."""
    encoding = resp.encoding or "utf-8"

    try:
        return body.decode(
            encoding,
            errors="replace",
        )
    except (LookupError, UnicodeError):
        return body.decode(
            "utf-8",
            errors="replace",
        )


def _get_bounded(
    session: requests.Session,
    url: str,
) -> tuple[requests.Response, bytes]:
    """
    Fetch a response using streaming and read only the
    configured maximum number of response-body bytes.
    """
    resp = session.get(
        url,
        timeout=settings.request_timeout,
        allow_redirects=False,
        stream=True,
    )

    try:
        body = _read_bounded_body(resp)
        return resp, body
    except Exception:
        resp.close()
        raise


def _title_from_text(text: str) -> str | None:
    match = TITLE_RE.search(text)

    if match:
        return re.sub(
            r"\s+",
            " ",
            match.group(1),
        ).strip()[:300]

    try:
        soup = BeautifulSoup(
            text,
            "html.parser",
        )

        return (
            soup.title.get_text(
                " ",
                strip=True,
            )[:300]
            if soup.title
            else None
        )

    except Exception:
        return None


def _visible_text_from_text(text: str) -> str:
    try:
        soup = BeautifulSoup(
            text,
            "html.parser",
        )

        for tag in soup(["script", "style"]):
            tag.decompose()

        return soup.get_text(
            " ",
            strip=True,
        )[:20_000]

    except Exception:
        return text[:20_000]


def _check_exposed_paths(
    session: requests.Session,
    base: str,
) -> list[dict]:

    found = []

    for path, meta in EXPOSED_PATH_CHECKS.items():

        try:
            resp, body = _get_bounded(
                session,
                urljoin(base, path),
            )

        except requests.RequestException:
            continue

        try:
            if resp.status_code != 200:
                continue

            body_sample = _decode_body(
                body[:20_000],
                resp,
            )

            matched = True

            if meta["match"] is not None:
                matched = any(
                    marker.lower()
                    in body_sample.lower()
                    for marker in meta["match"]
                )

            if matched:
                found.append(
                    {
                        "type": meta["type"],
                        "value": path,
                        "severity": meta["severity"],
                        "confidence": (
                            0.9
                            if meta["match"]
                            else 0.6
                        ),
                        "evidence": (
                            f"GET {path} returned HTTP 200"
                            + (
                                " and matched expected content"
                                if meta["match"]
                                else
                                " (content-based confirmation "
                                "not available)"
                            )
                        ),
                    }
                )

        finally:
            resp.close()

    return found


def _tls_fingerprint(
    target: str,
) -> dict | None:
    """
    Collect a certificate fingerprint when direct TLS access is
    available. Certificate verification is intentionally disabled
    because this function observes certificate metadata rather than
    validating trust.
    """
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        with socket.create_connection(
            (target, 443),
            timeout=settings.request_timeout,
        ) as sock:

            with ctx.wrap_socket(
                sock,
                server_hostname=target,
            ) as ssock:

                der_cert = ssock.getpeercert(
                    binary_form=True
                )

                cert_sha256 = hashlib.sha256(
                    der_cert
                ).hexdigest()

                cert = ssock.getpeercert()

                return {
                    "cert_sha256": cert_sha256,
                    "cert_info": cert,
                }

    except Exception:
        return None


def probe(
    target: str,
    db_path: str | None = None,
) -> dict:

    target = target.strip().lower()

    if not is_valid_onion_v3(target):
        raise ValueError(
            f"Invalid target: '{target}' is not a valid "
            "v3 onion address "
            "(expected a valid 56-character Tor v3 "
            "address followed by .onion)"
        )

    base = f"http://{target}/"

    session = requests.Session()

    session.proxies.update(
        {
            "http": settings.socks_proxy,
            "https": settings.socks_proxy,
        }
    )

    session.headers.update(
        {
            "User-Agent": "SIH-Lab-Research/0.1"
        }
    )

    observed_at = datetime.now(
        timezone.utc
    ).isoformat()

    r, body = _get_bounded(
        session,
        base,
    )

    try:
        text = _decode_body(
            body,
            r,
        )

        body_hash = sha256_bytes(body)
        title = _title_from_text(text)
        page_text = _visible_text_from_text(text)

        server = r.headers.get("Server")
        ctype = r.headers.get("Content-Type")

        content_length = r.headers.get(
            "Content-Length",
            "",
        )

        if content_length.isdigit():
            clen = int(content_length)
        else:
            clen = len(body)

        favicon_hash = None

        try:
            fr, favicon_body = _get_bounded(
                session,
                urljoin(
                    base,
                    "/favicon.ico",
                ),
            )

            try:
                if fr.ok and favicon_body:
                    favicon_hash = sha256_bytes(
                        favicon_body
                    )
            finally:
                fr.close()

        except requests.RequestException:
            pass

        path_indicators = _check_exposed_paths(
            session,
            base,
        )

        status_exposed = any(
            indicator["type"]
            == "EXPOSED_SERVER_STATUS"
            for indicator in path_indicators
        )

        indicators = list(path_indicators)

        if server:
            indicators.append(
                {
                    "type": "SERVER_BANNER",
                    "value": server,
                    "severity": "info",
                    "confidence": 0.99,
                    "evidence": (
                        "Server response header"
                    ),
                }
            )

        if title and any(
            pattern.lower() in title.lower()
            for pattern in DEFAULT_PAGE_PATTERNS
        ):
            indicators.append(
                {
                    "type": "DEFAULT_WEB_PAGE",
                    "value": title,
                    "severity": "medium",
                    "confidence": 0.95,
                    "evidence": (
                        "Page title matches a known "
                        "default-page pattern"
                    ),
                }
            )

        classification = classify(
            f"{title or ''} {page_text}"
        )

        tls = _tls_fingerprint(target)

        tls_cert_sha256 = (
            tls["cert_sha256"]
            if tls
            else None
        )

        infra_linking = (
            build_infrastructure_linking_clue(
                tls_cert_sha256
            )
        )

        wallets_found = extract_wallets(
            page_text
        )

        wallet_correlations = [
            {
                **wallet,
                "correlation": correlate_wallet(
                    wallet["address"]
                ),
            }
            for wallet in wallets_found
        ]

        result = {
            "target": target,
            "observed_at": observed_at,
            "http": {
                "status": r.status_code,
                "server": server,
                "content_type": ctype,
                "content_length": clen,
                "page_title": title,
            },
            "fingerprints": {
                "body_sha256": body_hash,
                "favicon_sha256": favicon_hash,
            },
            "server_status": {
                "exposed": status_exposed,
                "test": f"HTTP {r.status_code}",
            },
            "exposed_paths_checked": len(
                EXPOSED_PATH_CHECKS
            ),
            "indicators": indicators,
            "classification": classification,
            "tls": (
                {
                    "cert_sha256": tls_cert_sha256
                }
                if tls
                else None
            ),
            "infrastructure_linking": infra_linking,
            "wallets_detected": wallet_correlations,
        }

        con = connect(db_path)

        cur = con.execute(
            """
            INSERT OR IGNORE INTO observations(
                target,
                observed_at,
                http_status,
                server_header,
                content_type,
                content_length,
                page_title,
                body_sha256,
                favicon_sha256,
                server_status_exposed,
                evidence_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                target,
                observed_at,
                r.status_code,
                server,
                ctype,
                clen,
                title,
                body_hash,
                favicon_hash,
                int(status_exposed),
                json.dumps(result),
            ),
        )

        obs_id = cur.lastrowid

        if obs_id:
            con.executemany(
                """
                INSERT INTO indicators(
                    observation_id,
                    indicator_type,
                    value,
                    severity,
                    confidence,
                    evidence
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        obs_id,
                        indicator["type"],
                        indicator["value"],
                        indicator["severity"],
                        indicator["confidence"],
                        indicator["evidence"],
                    )
                    for indicator in indicators
                ],
            )

        con.commit()
        con.close()

        return result

    finally:
        r.close()


def probe_batch(
    targets: list[str],
    db_path: str | None = None,
) -> list[dict]:

    results = []

    for index, target in enumerate(targets):

        try:
            results.append(
                probe(
                    target,
                    db_path=db_path,
                )
            )

        except Exception as exc:
            results.append(
                {
                    "target": target,
                    "error": (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
                }
            )

        if index < len(targets) - 1:
            time.sleep(
                settings.batch_delay_seconds
            )

    return results
