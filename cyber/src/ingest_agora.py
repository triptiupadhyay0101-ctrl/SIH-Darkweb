"""
Ingest the Agora darknet marketplace dataset.

The Agora dataset is a historical 2014-2015 marketplace corpus used only
for offline research and classifier validation. It is not used to access
or interact with live darknet services.

The dataset informed the real-corpus-validated keyword coverage in
classify.py for drugs, weapons, hacking_services, data_theft, and fraud.
"""

from __future__ import annotations

import csv

from .db import connect


def _ensure_agora_table(con):
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS agora_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT,
            category TEXT,
            item TEXT,
            description TEXT,
            price TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_agora_category
        ON agora_listings(category);
        """
    )
    con.commit()


def ingest(path: str, db_path: str | None = None) -> int:
    """Import Agora CSV listings into SQLite and return row count."""

    con = connect(db_path)
    _ensure_agora_table(con)

    # Re-importing should produce a deterministic database state.
    con.execute("DELETE FROM agora_listings")

    count = 0
    batch = []

    with open(
        path,
        encoding="utf-8",
        errors="replace",
        newline="",
    ) as f:
        reader = csv.DictReader(f, skipinitialspace=True)

        for row in reader:
            batch.append(
                (
                    row.get("Vendor"),
                    row.get("Category"),
                    row.get("Item"),
                    row.get("Item Description"),
                    row.get("Price"),
                )
            )
            count += 1

            if len(batch) >= 5000:
                con.executemany(
                    """
                    INSERT INTO agora_listings
                    (vendor, category, item, description, price)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    batch,
                )
                batch = []

        if batch:
            con.executemany(
                """
                INSERT INTO agora_listings
                (vendor, category, item, description, price)
                VALUES (?, ?, ?, ?, ?)
                """,
                batch,
            )

    con.commit()
    con.close()

    return count
