"""
Rule-based threat classifier (first-pass, not ML).

Evidence basis:
- safe_corpus.pdf: real scraped forum-thread records, used to strengthen
  data-theft vocabulary.
- Agora.csv: historical marketplace listings used to validate category
  coverage and identify representative threat-related vocabulary.

Agora directly supports:
- drugs
- weapons
- hacking_services
- data_theft
- fraud

Credential-theft vocabulary is supported partially through account,
password, login, and credential-related listings.

Malware vocabulary is retained as a general defensive detection category.

This classifier provides threat-category signals, not proof of criminal
activity, identity, ownership, or attribution.
"""

from __future__ import annotations

import re


RULES = {
    "credential_theft": [
        r"\bpasswords?\b",
        r"\bpassword\s+list\b",
        r"\bpassword\s+dump\b",
        r"\bcredentials?\b",
        r"\bcredential\s+dump\b",
        r"\bstolen\s+credentials?\b",
        r"\bstolen\s+passwords?\b",
        r"\blogin(?:s)?\b",
        r"\blogin\s+access\b",
        r"\baccount\s+access\b",
        r"\baccount\s+credentials?\b",
        r"\bverified\s+account\b",
        r"\bverified\s+accounts\b",
        r"\bcookies?\b",
        r"\bsession\s+cookies?\b",
        r"\bvpn\s+access\b",
        r"\bemail\s+account\b",
        r"\bpaypal\s+account\b",
        r"\bcracked\s+accounts?\b",
        r"\bcracked\s+login\b",
        r"\bstolen\s+accounts?\b",
        r"\bstolen\s+login\b",
        r"\bemail\s+and\s+password\b",
        r"\bemail\s+\+\s+password\b",
        r"\busername\s+and\s+password\b",
        r"\blogin\s+details?\b",
        r"\baccount\s+details?\b",
        r"\baccount\s+information\b",
    ],

    "data_theft": [
        r"\bdatabase\b",
        r"\bdatabase\s+dump\b",
        r"\bdatabase\s+leak\b",
        r"\bdata\s+dump\b",
        r"\bstolen\s+data\b",
        r"\bstolen\s+information\b",
        r"\bdata\s+leak\b",
        r"\bdata\s+leaks\b",
        r"\bleaked\s+data\b",
        r"\bleaked\s+database\b",
        r"\bleaked\s+accounts?\b",
        r"\bleak(?:ed|s)?\b",
        r"\bcombolists?\b",
        r"\bcombo\s+lists?\b",
        r"\bemail\s+lists?\b",
        r"\bemail\s+database\b",
        r"\bpersonal\s+data\b",
        r"\bpersonal\s+information\b",
        r"\bidentity\s+data\b",
        r"\bdriver\s+licen[cs]e\b",
        r"\bssn\b",
        r"\bsocial\s+security\s+number\b",
        r"\brecords?\b",
        r"\brecord\s+dump\b",
        r"\bbreach(?:ed|es)?\b",
        r"\bdata/accounts?\b",
        r"\baccount\s+database\b",
        r"\bmillions?\s+of\s+emails?\b",
        r"\bmillions?\s+of\s+accounts?\b",
        r"\bemail\s+addresses?\b",
        r"\bemail\s+address\s+list\b",
        r"\bemail\s+database\b",
        r"\bbulk\s+email\b",
        r"\bemail\s+dataset\b",
        r"\bmillions?\s+of\s+emails?\b",
        r"\bmillions?\s+of\s+email\s+addresses?\b",
        r"\bdata\s+set\b",
        r"\bdataset\b",
        r"\buser\s+data\b",
        r"\bcustomer\s+data\b",
        r"\buser\s+records?\b",
    ],

    "malware": [
        r"\bransomware\b",
        r"\btrojan\b",
        r"\btrojans\b",
        r"\bbotnet\b",
        r"\bbotnets\b",
        r"\bbot\s*net\b",
        r"\bloader\b",
        r"\bloaders\b",
        r"\binfostealer\b",
        r"\binformation\s+stealer\b",
        r"\bstealer\s+malware\b",
        r"\bmalware\b",
        r"\bmalicious\s+software\b",
        r"\bremote\s+access\s+trojan\b",
        r"\brat\b",
    ],

    "fraud": [
        r"\bcredit\s+cards?\b",
        r"\bcredit\s+card\s+info\b",
        r"\bdebit\s+cards?\b",
        r"\bcarding\b",
        r"\bcardable\b",
        r"\bcvv(?:2)?\b",
        r"\bcvv/cvv2\b",
        r"\bpaypal\b",
        r"\bpaypal\s+accounts?\b",
        r"\bbank\s+accounts?\b",
        r"\bverified\s+paypal\b",
        r"\bverified\s+accounts?\b",
        r"\bvisa\b",
        r"\bmastercard\b",
        r"\bmaster\s*/?\s*visa\b",
        r"\brefund\s+service\b",
        r"\bamazon\s+refund\b",
        r"\bcash\s+out\b",
        r"\bcashout\b",
        r"\bdumps?\b",
        r"\btrack\s+2\b",
        r"\bwestern\s+union\b",
        r"\bmoney\s+transfer\b",
        r"\bfake\s+scans?\b",
        r"\bidentity\s+scan\b",
        r"\bfraud\b",
        r"\bscam(?:ming|s)?\b",
        r"\bcard\s+number\b",
        r"\bcard\s+details?\b",
        r"\baccount\s+holder\b",
    ],

    "hacking_services": [
        r"\bhacking\b",
        r"\bhack(?:ed|ing)?\b",
        r"\bhacking\s+service\b",
        r"\bhacking\s+services\b",
        r"\bhacking\s+guide\b",
        r"\bhacking\s+tutorial\b",
        r"\bhacking\s+ebook\b",
        r"\bhacking\s+ebooks\b",
        r"\bhack(?:ing)?\s+manual\b",
        r"\bfacebook\s+hacking\b",
        r"\baccount\s+hacking\b",
        r"\bemail\s+hacking\b",
        r"\batm\s+hacking\b",
        r"\bwifi\s+hacking\b",
        r"\bwi-fi\s+hacking\b",
        r"\bpassword\s+cracking\b",
        r"\bpassword\s+cracker\b",
        r"\bddos\b",
        r"\bddos\s+attack\b",
        r"\bddos\s+service\b",
        r"\bdenial\s+of\s+service\b",
        r"\bbotnet\b",
        r"\bbotnet\s+guide\b",
        r"\bexploit(?:s|ing)?\b",
        r"\bexploit\s+service\b",
        r"\baccount\s+creator\b",
        r"\baccount\s+creation\s+tool\b",
        r"\bverification\s+service\b",
        r"\bsms\s+verification\s+service\b",
        r"\bproxy\s+software\b",
        r"\bproxy\s+service\b",
        r"\bdevice\s+id\b",
        r"\bmac\s+address\s+changer\b",
    ],

    "drugs": [
        r"\bcocaine\b",
        r"\bheroin\b",
        r"\bfentanyl\b",
        r"\bmdma\b",
        r"\bmeth(?:amphetamine)?\b",
        r"\bweed\b",
        r"\bcannabis\b",
        r"\bkush\b",
        r"\blsd\b",
        r"\bketamine\b",
        r"\bopioids?\b",
        r"\bbenzos?\b",
        r"\bbenzodiazepines?\b",
        r"\bpills?\b",
        r"\becstasy\b",
        r"\bpsychedelics?\b",
        r"\bhash\b",
        r"\bmarijuana\b",
        r"\bconcentrates?\b",
        r"\bstimulants?\b",
        r"\bprescription\s+drugs?\b",
        r"\bprescription\s+medication\b",
        r"\bsteroids?\b",
        r"\bdrugs?\b",
        r"\bresearch chemicals?\b",
        r"\brcs?\b",
        r"\bfluoroamphetamine\b",
        r"\bamphetamine\b",
        r"\bmdpv\b",
        r"\bmdpbp\b",
        r"\bmddmv\b",
        r"\b4-fma\b",
        r"\b3-fa\b",
        r"\b4-fmc\b",
        r"\b4-bmc\b",
        r"\b4-fa\b",
        r"\b2-fa\b",
        r"\b2-fma\b",
        r"\balpha-pvp\b",
        r"\bα-pvp\b",
    ],

    "weapons": [
        r"\bfirearms?\b",
        r"\bweapons?\b",
        r"\brifles?\b",
        r"\bpistols?\b",
        r"\bhandguns?\b",
        r"\bglock\b",
        r"\bammunition\b",
        r"\bammo\b",
        r"\bguns?\b",
        r"\bmagazines?\b",
        r"\bknives?\b",
        r"\bknife\b",
        r"\bstun\s+guns?\b",
        r"\btasers?\b",
        r"\bexplosives?\b",
        r"\bgrenades?\b",
        r"\bshotguns?\b",
        r"\brevolvers?\b",
        r"\bautomatic\s+weapons?\b",
        r"\blethal\s+firearms?\b",
    ],
}


def classify(text: str) -> dict:
    """Return matched threat categories with evidence counts/confidence."""

    if not isinstance(text, str):
        text = str(text)

    normalized = text.lower()

    scores = {
        category: sum(
            bool(re.search(pattern, normalized))
            for pattern in patterns
        )
        for category, patterns in RULES.items()
    }

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    total = sum(scores.values()) or 1

    return {
        "labels": [
            {
                "category": category,
                "evidence_count": count,
                "confidence": round(count / total, 3),
            }
            for category, count in ranked
            if count
        ]
    }
