"""
Infrastructure linking: correlate a TLS certificate fingerprint (if the onion
service happens to serve HTTPS directly, or if a known clearnet cert hash is
supplied) against public Certificate Transparency logs via crt.sh.

This is the mechanism specified in the PS: "SSL certificates tied to clearnet
domains ... matching them with clearnet infrastructure to point to the likely
origin servers."

No API key required — crt.sh is a free public CT-log search service.
"""
from __future__ import annotations
import requests


def crtsh_lookup_by_sha256(cert_sha256: str, timeout: float = 15.0) -> list[dict]:
    """
    Query crt.sh for certificates matching a given SHA-256 fingerprint.
    Returns a list of matching certificate records (issuer, common name,
    matching domains) if the same cert is registered for a clearnet domain.
    Empty list = no clearnet match found (does not mean the cert is unused,
    only that it isn't in public CT logs, e.g. self-signed certs on onions
    are typically NOT logged).
    """
    url = f"https://crt.sh/?sha256={cert_sha256}&output=json"
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": "SIH-Lab-Research/0.1"})
        if resp.status_code != 200 or not resp.text.strip():
            return []
        return resp.json()
    except Exception:
        return []


def crtsh_lookup_by_domain(domain: str, timeout: float = 15.0) -> list[dict]:
    """
    Query crt.sh for all certificates ever issued for a clearnet domain.
    Useful when you already suspect a clearnet domain and want to see if it
    shares infrastructure history with your onion target.
    """
    url = f"https://crt.sh/?q={domain}&output=json"
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": "SIH-Lab-Research/0.1"})
        if resp.status_code != 200 or not resp.text.strip():
            return []
        return resp.json()
    except Exception:
        return []


def build_infrastructure_linking_clue(cert_sha256: str | None) -> dict:
    """
    Given a TLS cert SHA-256 (from probe._tls_fingerprint), attempt clearnet
    correlation. Returns a structured clue for the backend/AI correlation
    layer — this is the PS item 3 deliverable: "identify clues that may
    connect an onion service with related clearnet infrastructure."
    """
    if not cert_sha256:
        return {
            "correlation_attempted": False,
            "reason": "No TLS certificate available (most onion services serve plain HTTP only)",
            "matches": [],
        }
    matches = crtsh_lookup_by_sha256(cert_sha256)
    return {
        "correlation_attempted": True,
        "method": "certificate_transparency_sha256_match",
        "source": "crt.sh",
        "matches": [
            {
                "common_name": m.get("common_name"),
                "name_value": m.get("name_value"),
                "issuer_name": m.get("issuer_name"),
                "not_before": m.get("not_before"),
                "not_after": m.get("not_after"),
            }
            for m in matches
        ],
        "match_count": len(matches),
        "confidence": "medium" if matches else "none",
        "evidence": (
            f"TLS certificate SHA-256 {cert_sha256} found in {len(matches)} "
            f"public Certificate Transparency log entries"
            if matches else
            "No public CT log match — either no clearnet reuse, or cert is self-signed/unlogged"
        ),
    }
