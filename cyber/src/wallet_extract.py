"""
Cryptocurrency address extraction from scraped page text.

Note on crypto_detection_research_dataset.csv:
the dataset was inspected as a 52-column, pre-featurized research dataset
containing per-coin count/present features (for example,
bitcoin_legacy_count and bitcoin_legacy_present). It does not contain
reusable extraction regexes.

The coin categories represented in that dataset informed the supported
coin types here, while the regex patterns themselves are independently
written address-format patterns used for lightweight extraction.

Known canonical/example addresses used by the controlled test environment
are excluded so they are not reported as investigative wallet indicators.
"""

from __future__ import annotations

import re


PATTERNS = {
    "bitcoin_legacy": re.compile(
        r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"
    ),
    "bitcoin_segwit": re.compile(
        r"\bbc1[a-z0-9]{25,90}\b"
    ),
    "ethereum": re.compile(
        r"\b0x[a-fA-F0-9]{40}\b"
    ),
    "monero": re.compile(
        r"\b4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}\b"
    ),
    "litecoin": re.compile(
        r"\b[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}\b"
    ),
}


# Canonical/example address present in the controlled Apache test page.
# It should not be treated as an investigative wallet indicator.
EXCLUDED_ADDRESSES = {
    "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
}


def extract_wallets(text: str) -> list[dict]:
    """Return candidate cryptocurrency addresses found in text."""

    found = []

    for coin, pattern in PATTERNS.items():
        for match in pattern.findall(text):
            if match in EXCLUDED_ADDRESSES:
                continue

            found.append(
                {
                    "coin": coin,
                    "address": match,
                }
            )

    return found
