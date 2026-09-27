import csv
from .db import connect

def ingest(path: str, db_path: str | None = None) -> int:
    rows=[]
    with open(path, newline="", encoding="utf-8") as f:
        reader=csv.DictReader((line for line in f if not line.lstrip().startswith("#")))
        for row in reader:
            rows.append((row["date"], int(row["onions"]), float(row["frac"]) if row.get("frac") else None))
    con=connect(db_path)
    con.executemany("INSERT OR REPLACE INTO tor_metrics(date,onions,frac) VALUES(?,?,?)", rows)
    con.commit(); con.close()
    return len(rows)
