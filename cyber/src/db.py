import sqlite3
from pathlib import Path
from .config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    http_status INTEGER,
    server_header TEXT,
    content_type TEXT,
    content_length INTEGER,
    page_title TEXT,
    body_sha256 TEXT,
    favicon_sha256 TEXT,
    server_status_exposed INTEGER NOT NULL DEFAULT 0,
    evidence_json TEXT NOT NULL,
    UNIQUE(target, observed_at)
);
CREATE TABLE IF NOT EXISTS indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    observation_id INTEGER NOT NULL,
    indicator_type TEXT NOT NULL,
    value TEXT,
    severity TEXT NOT NULL,
    confidence REAL NOT NULL,
    evidence TEXT NOT NULL,
    FOREIGN KEY(observation_id) REFERENCES observations(id)
);
CREATE TABLE IF NOT EXISTS tor_metrics (
    date TEXT PRIMARY KEY,
    onions INTEGER NOT NULL,
    frac REAL
);
CREATE TABLE IF NOT EXISTS graph_nodes (
    node_id TEXT PRIMARY KEY,
    bipartite INTEGER,
    node_type TEXT,
    domain TEXT,
    path TEXT,
    category TEXT,
    subcategory TEXT,
    lang TEXT,
    url TEXT,
    value TEXT,
    network TEXT
);
CREATE TABLE IF NOT EXISTS graph_edges (
    source TEXT NOT NULL,
    target TEXT NOT NULL,
    PRIMARY KEY(source, target)
);
"""

def connect(path: str | None = None):
    db = Path(path or settings.db_path)
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db)
    con.execute("PRAGMA foreign_keys=ON")
    return con

def init_db(path: str | None = None):
    con = connect(path)
    con.executescript(SCHEMA)
    con.commit()
    con.close()
