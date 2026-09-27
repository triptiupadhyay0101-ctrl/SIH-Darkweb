"""
Correlate a cryptocurrency wallet address observed on a scanned onion page
with wallet identifier nodes imported from the bipartite onion/identifier
graph.

Important:
- Elliptic `tx_id` values represent transaction identifiers, not wallet
  addresses.
- Therefore, an observed wallet address is NOT passed to the Elliptic
  transaction lookup.
- A successful match here means the address exists as an identifier node in
  the imported graph. It is a correlation signal, not proof of ownership
  or attribution.
"""

from __future__ import annotations

from .db import connect


def correlate_wallet(address: str, db_path: str | None = None) -> dict:
    """Correlate an observed wallet address with imported wallet identifiers."""

    con = connect(db_path)

    row = con.execute(
        """
        SELECT node_id, node_type, value, network
        FROM graph_nodes
        WHERE value = ?
          AND node_type LIKE '%Wallet%'
        LIMIT 1
        """,
        (address,),
    ).fetchone()

    con.close()

    if row:
        return {
            "address": address,
            "source": "bipartite_onion_identifier_graph",
            "match_found": True,
            "node_id": row[0],
            "node_type": row[1],
            "network": row[3],
            "confidence": "medium",
            "evidence": (
                "Address matches a wallet identifier node in the "
                "onion<->identifier relationship graph"
            ),
        }

    return {
        "address": address,
        "match_found": False,
        "confidence": "none",
        "evidence": (
            "No matching wallet identifier node was found in the "
            "bipartite onion/identifier graph"
        ),
    }
