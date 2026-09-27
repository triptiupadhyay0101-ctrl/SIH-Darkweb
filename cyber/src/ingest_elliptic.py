"""
Ingest the Elliptic Bitcoin transaction-graph dataset:
- edgelist: transaction -> transaction graph edges
- classes: illicit(1) / licit(2) / unknown label per transaction
- features pt1-4: 165 anonymized features + timestep per transaction
  (split across 4 files, no header row in the feature files)

This gives the infrastructure-linking layer a real, labeled wallet/transaction
graph to cross-reference against any BTC address found on a scanned onion page.
"""
from __future__ import annotations
import csv
import openpyxl
from .db import connect

FEATURE_COLS = 167  # txId, timestep, + 165 features


def _ensure_elliptic_tables(con):
    con.executescript("""
    CREATE TABLE IF NOT EXISTS elliptic_edges (
        tx_id1 TEXT NOT NULL,
        tx_id2 TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_elliptic_edges_tx1 ON elliptic_edges(tx_id1);
    CREATE INDEX IF NOT EXISTS idx_elliptic_edges_tx2 ON elliptic_edges(tx_id2);

    CREATE TABLE IF NOT EXISTS elliptic_classes (
        tx_id TEXT PRIMARY KEY,
        label TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS elliptic_features (
        tx_id TEXT PRIMARY KEY,
        timestep INTEGER
    );
    """)
    con.commit()


def ingest_edgelist(path: str, db_path: str | None = None) -> int:
    con = connect(db_path)
    _ensure_elliptic_tables(con)
    con.execute("DELETE FROM elliptic_edges")
    count = 0
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # header: txId1,txId2
        batch = []
        for row in reader:
            if len(row) < 2:
                continue
            batch.append((row[0], row[1]))
            count += 1
            if len(batch) >= 5000:
                con.executemany("INSERT INTO elliptic_edges(tx_id1, tx_id2) VALUES (?, ?)", batch)
                batch = []
        if batch:
            con.executemany("INSERT INTO elliptic_edges(tx_id1, tx_id2) VALUES (?, ?)", batch)
    con.commit()
    con.close()
    return count


def ingest_classes(path: str, db_path: str | None = None) -> int:
    con = connect(db_path)
    _ensure_elliptic_tables(con)
    con.execute("DELETE FROM elliptic_classes")
    count = 0
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # header: txId,class
        batch = []
        for row in reader:
            if len(row) < 2:
                continue
            batch.append((row[0], row[1]))
            count += 1
            if len(batch) >= 5000:
                con.executemany("INSERT OR REPLACE INTO elliptic_classes(tx_id, label) VALUES (?, ?)", batch)
                batch = []
        if batch:
            con.executemany("INSERT OR REPLACE INTO elliptic_classes(tx_id, label) VALUES (?, ?)", batch)
    con.commit()
    con.close()
    return count


def ingest_features_xlsx(path: str, db_path: str | None = None) -> int:
    """Each features file has no header: col1=txId, col2=timestep, col3-167=features (ignored for now)."""
    con = connect(db_path)
    _ensure_elliptic_tables(con)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    count = 0
    batch = []
    for row in ws.iter_rows(values_only=True):
        if row[0] is None:
            continue
        tx_id = str(row[0])
        timestep = row[1]
        batch.append((tx_id, timestep))
        count += 1
        if len(batch) >= 5000:
            con.executemany("INSERT OR REPLACE INTO elliptic_features(tx_id, timestep) VALUES (?, ?)", batch)
            batch = []
    if batch:
        con.executemany("INSERT OR REPLACE INTO elliptic_features(tx_id, timestep) VALUES (?, ?)", batch)
    wb.close()
    con.commit()
    con.close()
    return count


def lookup_tx(tx_id: str, db_path: str | None = None) -> dict | None:
    """Look up a single transaction ID: its illicit/licit label and known timestep."""
    con = connect(db_path)
    row = con.execute(
        "SELECT c.label, f.timestep FROM elliptic_classes c "
        "LEFT JOIN elliptic_features f ON f.tx_id = c.tx_id WHERE c.tx_id = ?",
        (tx_id,),
    ).fetchone()
    con.close()
    if not row:
        return None
    label_map = {"1": "illicit", "2": "licit", "unknown": "unknown"}
    return {"tx_id": tx_id, "label": label_map.get(row[0], row[0]), "timestep": row[1]}
