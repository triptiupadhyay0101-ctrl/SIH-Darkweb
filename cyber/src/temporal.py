"""
Temporal and migration analysis.

This module compares repeated HTTP-level observations of the same
authorized onion service over time.

It detects:
- server-banner changes
- content fingerprint changes
- favicon changes
- availability changes
- possible infrastructure migration signals

Descriptor-level Tor analysis is intentionally out of scope here.
"""
from __future__ import annotations

from .db import connect


def analyze_target_history(
    target: str,
    db_path: str | None = None,
) -> dict:
    """Analyze historical observations for one target."""
    con = connect(db_path)

    rows = con.execute(
        """
        SELECT
            observed_at,
            server_header,
            body_sha256,
            favicon_sha256,
            http_status
        FROM observations
        WHERE target = ?
        ORDER BY observed_at ASC
        """,
        (target,),
    ).fetchall()

    con.close()

    if not rows:
        return {
            "target": target,
            "observation_count": 0,
            "changes": [],
            "migration_signals": [],
        }

    changes = []
    migration_signals = []

    previous = rows[0]

    for current in rows[1:]:
        (
            prev_observed_at,
            prev_server,
            prev_body,
            prev_favicon,
            prev_status,
        ) = previous

        (
            curr_observed_at,
            curr_server,
            curr_body,
            curr_favicon,
            curr_status,
        ) = current

        # Server banner change
        if curr_server != prev_server:
            change = {
                "type": "SERVER_BANNER_CHANGE",
                "at": curr_observed_at,
                "from": prev_server,
                "to": curr_server,
                "confidence": 0.9,
                "evidence": (
                    "Server response header changed between observations"
                ),
            }
            changes.append(change)
            migration_signals.append({
                "type": "POSSIBLE_INFRASTRUCTURE_CHANGE",
                "at": curr_observed_at,
                "confidence": 0.9,
                "evidence": (
                    "Server banner changed, indicating a possible "
                    "backend or hosting change"
                ),
            })

        # Content fingerprint change
        if curr_body != prev_body:
            changes.append({
                "type": "CONTENT_FINGERPRINT_CHANGE",
                "at": curr_observed_at,
                "from": prev_body,
                "to": curr_body,
                "confidence": 0.85,
                "evidence": "Page body SHA-256 changed",
            })

        # Favicon change
        if curr_favicon != prev_favicon:
            changes.append({
                "type": "FAVICON_CHANGE",
                "at": curr_observed_at,
                "from": prev_favicon,
                "to": curr_favicon,
                "confidence": 0.7,
                "evidence": "Favicon SHA-256 changed",
            })

        # Availability change
        if curr_status != prev_status:
            changes.append({
                "type": "AVAILABILITY_CHANGE",
                "at": curr_observed_at,
                "from": prev_status,
                "to": curr_status,
                "confidence": 0.6,
                "evidence": (
                    "HTTP status code changed between observations"
                ),
            })

        previous = current

    return {
        "target": target,
        "first_seen": rows[0][0],
        "last_seen": rows[-1][0],
        "observation_count": len(rows),
        "changes": changes,
        "migration_signals": migration_signals,
        "infrastructure_stable": len(migration_signals) == 0,
    }
