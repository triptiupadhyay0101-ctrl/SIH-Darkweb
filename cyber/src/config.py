from dataclasses import dataclass
import base64
import hashlib
import os
import re
from urllib.parse import urlparse


def _positive_float(value: str, name: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"{name} must be a positive number"
        ) from exc

    if parsed <= 0:
        raise ValueError(
            f"{name} must be greater than 0"
        )

    return parsed


def _bounded_int(
    value: str,
    name: str,
    minimum: int,
    maximum: int,
) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"{name} must be an integer"
        ) from exc

    if not minimum <= parsed <= maximum:
        raise ValueError(
            f"{name} must be between "
            f"{minimum} and {maximum}"
        )

    return parsed


def _valid_socks_proxy(value: str) -> str:
    parsed = urlparse(value)

    if parsed.scheme not in {
        "socks5",
        "socks5h",
    }:
        raise ValueError(
            "SOCKS_PROXY must use socks5:// "
            "or socks5h://"
        )

    if not parsed.hostname:
        raise ValueError(
            "SOCKS_PROXY must contain a hostname"
        )

    if parsed.path not in {"", "/"}:
        raise ValueError(
            "SOCKS_PROXY must not contain a path"
        )

    return value


@dataclass(frozen=True)
class Settings:
    db_path: str = os.getenv(
        "SIH_DB",
        "module.db",
    )

    socks_proxy: str = _valid_socks_proxy(
        os.getenv(
            "SOCKS_PROXY",
            "socks5h://127.0.0.1:9050",
        )
    )

    request_timeout: float = _positive_float(
        os.getenv("REQUEST_TIMEOUT", "30"),
        "REQUEST_TIMEOUT",
    )

    max_body_bytes: int = _bounded_int(
        os.getenv("MAX_BODY_BYTES", "2000000"),
        "MAX_BODY_BYTES",
        minimum=1024,
        maximum=10_000_000,
    )

    batch_delay_seconds: float = _positive_float(
        os.getenv("BATCH_DELAY_SECONDS", "0.5"),
        "BATCH_DELAY_SECONDS",
    )


settings = Settings()


ONION_V3_RE = re.compile(
    r"^[a-z2-7]{56}\.onion$"
)


def is_valid_onion_v3(address: str) -> bool:
    """Validate the structure and checksum of a Tor v3 onion address."""
    address = address.strip().lower()

    if not ONION_V3_RE.fullmatch(address):
        return False

    encoded = address[:-6]

    try:
        decoded = base64.b32decode(
            encoded.upper(),
            casefold=True,
        )
    except (ValueError, base64.binascii.Error):
        return False

    if len(decoded) != 35:
        return False

    public_key = decoded[:32]
    checksum = decoded[32:34]
    version = decoded[34]

    if version != 0x03:
        return False

    expected_checksum = hashlib.sha3_256(
        b".onion checksum"
        + public_key
        + bytes([version])
    ).digest()[:2]

    return checksum == expected_checksum
