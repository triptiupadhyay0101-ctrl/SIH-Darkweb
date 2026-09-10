"""
Validation script for first-pass classifier coverage on the historical
Agora marketplace corpus.

Important:
This measures category-hit coverage, NOT ML accuracy or forensic
ground truth. Agora categories are historical marketplace labels and
some categories contain mixed content.

Data-theft is intentionally excluded from this Agora benchmark because
the Data/Accounts category contains heterogeneous account/subscription
listings and is not a clean data-theft ground truth.
"""

from src.db import connect
from src.classify import classify


EXPECTED_MAPPING = {
    "drugs": lambda c: c.lower().startswith("drugs/"),
    "weapons": lambda c: c.lower().startswith("weapons/"),
    "hacking_services": lambda c: c.lower() == "services/hacking",
    "fraud": lambda c: c.lower() == "services/money",
}


def run_validation(db_path: str | None = None, sample_size: int = 100):
    con = connect(db_path)

    rows = con.execute(
        """
        SELECT category, item, description
        FROM agora_listings
        """
    ).fetchall()

    con.close()

    per_category = {
        label: {"n": 0, "hits": 0}
        for label in EXPECTED_MAPPING
    }

    for category, item, desc in rows:

        for expected_label, matcher in EXPECTED_MAPPING.items():

            if not matcher(category or ""):
                continue

            if per_category[expected_label]["n"] >= sample_size:
                continue

            text = f"{item or ''} {desc or ''}"

            result = classify(text)

            fired = {
                label["category"]
                for label in result["labels"]
            }

            per_category[expected_label]["n"] += 1

            if expected_label in fired:
                per_category[expected_label]["hits"] += 1

            break

    total_n = sum(
        stats["n"]
        for stats in per_category.values()
    )

    total_hits = sum(
        stats["hits"]
        for stats in per_category.values()
    )

    overall = (
        round(100 * total_hits / total_n, 1)
        if total_n
        else 0
    )

    print(
        f"Overall coverage: "
        f"{total_hits}/{total_n} ({overall}%)\n"
    )

    for category, stats in per_category.items():

        rate = (
            round(100 * stats["hits"] / stats["n"], 1)
            if stats["n"]
            else 0
        )

        print(
            f"  {category:20s}: "
            f"{stats['hits']}/{stats['n']} ({rate}%)"
        )


if __name__ == "__main__":
    run_validation()
