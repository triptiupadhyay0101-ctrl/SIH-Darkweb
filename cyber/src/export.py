from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from .db import connect
from .temporal import analyze_target_history


def _rows_as_dicts(con, query, params=()):
    cur = con.execute(query, params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def export_json(out_path: str, db_path: str | None = None) -> str:
    con = connect(db_path)
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "observations": _rows_as_dicts(
            con,
            "SELECT * FROM observations ORDER BY id",
        ),
        "indicators": _rows_as_dicts(
            con,
            "SELECT * FROM indicators ORDER BY id",
        ),
    }
    con.close()

    Path(out_path).write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )
    return out_path


def export_csv(out_path: str, db_path: str | None = None) -> str:
    con = connect(db_path)

    rows = _rows_as_dicts(
        con,
        """
        SELECT
            o.target,
            o.observed_at,
            o.http_status,
            o.server_header,
            o.page_title,
            o.body_sha256,
            o.favicon_sha256,
            o.server_status_exposed,
            i.indicator_type,
            i.value,
            i.severity,
            i.confidence,
            i.evidence
        FROM observations o
        LEFT JOIN indicators i
            ON i.observation_id = o.id
        ORDER BY o.id
        """,
    )

    con.close()

    if not rows:
        Path(out_path).write_text("", encoding="utf-8")
        return out_path

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)

    return out_path


def _confidence_label(value: float) -> str:
    if value >= 0.85:
        return "High"
    if value >= 0.60:
        return "Medium"
    if value > 0:
        return "Low"
    return "None"


def _safe_json(value):
    if not value:
        return {}
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return {}


def _latest_observation(observations: list[dict]) -> dict:
    return max(
        observations,
        key=lambda row: row.get("observed_at") or "",
    )


def _collect_indicators(con, observation_ids: list[int]) -> list[dict]:
    if not observation_ids:
        return []

    placeholders = ",".join("?" for _ in observation_ids)

    return _rows_as_dicts(
        con,
        f"""
        SELECT
            observation_id,
            indicator_type,
            value,
            severity,
            confidence,
            evidence
        FROM indicators
        WHERE observation_id IN ({placeholders})
        ORDER BY
            CASE severity
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END,
            id
        """,
        observation_ids,
    )


def _collect_latest_evidence(observation: dict) -> dict:
    return _safe_json(observation.get("evidence_json"))


def _write_target_report(
    lines: list[str],
    con,
    target: str,
    observations: list[dict],
    db_path: str | None,
):
    observations = sorted(
        observations,
        key=lambda row: row.get("observed_at") or "",
    )

    latest = _latest_observation(observations)
    latest_evidence = _collect_latest_evidence(latest)

    observation_ids = [
        row["id"]
        for row in observations
        if row.get("id") is not None
    ]

    indicators = _collect_indicators(
        con,
        observation_ids,
    )

    lines.extend([
        f"## Target: `{target}`",
        "",
        "### Observation Summary",
        f"- First observed: {observations[0]['observed_at']}",
        f"- Last observed: {observations[-1]['observed_at']}",
        f"- Total observations: {len(observations)}",
        "",
        "### Latest Observation",
        f"- Observed at: {latest['observed_at']}",
        f"- HTTP status: {latest['http_status']}",
        f"- Server: {latest['server_header'] or 'Not disclosed'}",
        f"- Content type: {latest['content_type'] or 'Unknown'}",
        f"- Content length: {latest['content_length']}",
        f"- Page title: {latest['page_title'] or 'None'}",
        "",
        "### Current Fingerprints",
        f"- Body SHA-256: `{latest['body_sha256']}`",
        f"- Favicon SHA-256: "
        f"`{latest['favicon_sha256'] or 'None'}`",
        f"- Server-status exposed: "
        f"{bool(latest['server_status_exposed'])}",
        "",
        "### Security Indicators",
    ])

    unique_indicators = {}
    for indicator in indicators:
        key = (
            indicator["indicator_type"],
            indicator["value"],
        )
        unique_indicators[key] = indicator

    if unique_indicators:
        for indicator in unique_indicators.values():
            confidence = float(indicator["confidence"])

            lines.append(
                f"- **{indicator['indicator_type']}** "
                f"({indicator['severity'].upper()}, "
                f"{_confidence_label(confidence)}, "
                f"{confidence:.2f})"
            )
            lines.append(
                f"  - Value: `{indicator['value']}`"
            )
            lines.append(
                f"  - Evidence: {indicator['evidence']}"
            )
    else:
        lines.append(
            "- No infrastructure security indicators recorded."
        )

    lines.extend([
        "",
        "### Threat Classification",
    ])

    classification = latest_evidence.get(
        "classification",
        {},
    )

    labels = classification.get("labels", [])

    if labels:
        for label in labels:
            category = label.get(
                "category",
                "unknown",
            )
            count = label.get(
                "evidence_count",
                0,
            )
            confidence = float(
                label.get("confidence", 0)
            )

            lines.append(
                f"- **{category}** — "
                f"{count} evidence signal(s), "
                f"{_confidence_label(confidence)} "
                f"confidence ({confidence:.2f})"
            )
    else:
        lines.append(
            "- No threat category signals detected."
        )

    lines.extend([
        "",
        "### Wallet Indicators",
    ])

    wallets = latest_evidence.get(
        "wallets_detected",
        [],
    )

    if wallets:
        for wallet in wallets:
            coin = wallet.get(
                "coin",
                "unknown",
            )
            address = wallet.get(
                "address",
                "",
            )
            correlation = wallet.get(
                "correlation",
                {},
            )

            lines.append(
                f"- **{coin}**: `{address}`"
            )

            if correlation.get("match_found"):
                lines.append(
                    "  - Graph correlation: match found"
                )
                lines.append(
                    f"  - Confidence: "
                    f"{correlation.get('confidence', 'unknown')}"
                )
                lines.append(
                    f"  - Evidence: "
                    f"{correlation.get('evidence', 'Not provided')}"
                )
            else:
                lines.append(
                    "  - Graph correlation: no matching "
                    "wallet identifier found"
                )
    else:
        lines.append(
            "- No wallet indicators detected."
        )

    lines.extend([
        "",
        "### Infrastructure Correlation",
    ])

    infrastructure = latest_evidence.get(
        "infrastructure_linking",
        {},
    )

    if infrastructure.get("correlation_attempted"):
        lines.append(
            f"- Method: "
            f"{infrastructure.get('method', 'Not specified')}"
        )
        lines.append(
            f"- Public CT matches: "
            f"{infrastructure.get('match_count', 0)}"
        )

        matches = infrastructure.get(
            "matches",
            [],
        )

        if matches:
            for match in matches:
                if match.get("common_name"):
                    lines.append(
                        f"- Candidate certificate name: "
                        f"`{match['common_name']}`"
                    )

                if match.get("name_value"):
                    lines.append(
                        f"- Certificate names: "
                        f"`{match['name_value']}`"
                    )
        else:
            lines.append(
                "- No public Certificate Transparency "
                "match found."
            )
    else:
        reason = infrastructure.get(
            "reason",
            "No TLS certificate was available "
            "for correlation.",
        )
        lines.append(
            f"- Correlation not attempted: {reason}"
        )

    lines.extend([
        "",
        "### Temporal Analysis",
    ])

    history = analyze_target_history(
        target,
        db_path=db_path,
    )

    lines.append(
        f"- First seen: "
        f"{history.get('first_seen', 'N/A')}"
    )
    lines.append(
        f"- Last seen: "
        f"{history.get('last_seen', 'N/A')}"
    )
    lines.append(
        f"- Observations analyzed: "
        f"{history.get('observation_count', 0)}"
    )
    lines.append(
        f"- Infrastructure stable: "
        f"{history.get('infrastructure_stable', False)}"
    )

    changes = history.get(
        "changes",
        [],
    )

    if changes:
        lines.append("- Detected changes:")

        for change in changes:
            lines.append(
                f"  - **{change['type']}** at "
                f"{change['at']} "
                f"(confidence "
                f"{change['confidence']:.2f})"
            )
            lines.append(
                f"    - {change['evidence']}"
            )
    else:
        lines.append(
            "- No observed historical changes."
        )

    migration_signals = history.get(
        "migration_signals",
        [],
    )

    if migration_signals:
        lines.append(
            "- Possible infrastructure migration signals:"
        )

        for signal in migration_signals:
            lines.append(
                f"  - {signal['type']} at "
                f"{signal['at']} "
                f"(confidence "
                f"{signal['confidence']:.2f})"
            )
    else:
        lines.append(
            "- No infrastructure migration signal detected."
        )

    lines.extend([
        "",
        "### Observation Timeline",
        "",
        "| # | Observed At | HTTP | Server | Body Fingerprint |",
        "|---:|---|---:|---|---|",
    ])

    for index, observation in enumerate(
        observations,
        start=1,
    ):
        body_hash = observation.get(
            "body_sha256",
            "",
        )
        short_hash = (
            body_hash[:12]
            if body_hash
            else "None"
        )

        lines.append(
            f"| {index} | "
            f"{observation['observed_at']} | "
            f"{observation['http_status']} | "
            f"{observation['server_header'] or 'Unknown'} | "
            f"`{short_hash}...` |"
        )

    lines.append("")


def export_report(
    out_path: str,
    db_path: str | None = None,
) -> str:
    """
    Generate a unified investigator-facing Markdown report.

    The report consolidates observations by target and includes
    infrastructure fingerprints, security indicators, threat
    classification, wallet correlations, infrastructure correlation,
    and temporal analysis.

    Correlation results are investigative signals and should not
    be interpreted as definitive attribution.
    """
    con = connect(db_path)

    observations = _rows_as_dicts(
        con,
        "SELECT * FROM observations ORDER BY observed_at",
    )

    indicator_count = con.execute(
        "SELECT COUNT(*) FROM indicators"
    ).fetchone()[0]

    grouped = defaultdict(list)

    for observation in observations:
        grouped[observation["target"]].append(
            observation
        )

    lines = [
        "# Dark-Web Infrastructure Intelligence Report",
        "",
        f"Generated: "
        f"{datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "This report summarizes observations from authorized "
        "or controlled research targets. Correlation results "
        "represent investigative leads and evidence signals, "
        "not definitive identity or attribution.",
        "",
        "## Executive Summary",
        "",
        f"- Unique targets: {len(grouped)}",
        f"- Total observations: {len(observations)}",
        f"- Recorded indicators: {indicator_count}",
        "",
    ]

    if not observations:
        lines.append(
            "No observations are currently available."
        )
    else:
        for target, target_observations in grouped.items():
            _write_target_report(
                lines,
                con,
                target,
                target_observations,
                db_path,
            )

    lines.extend([
        "## Interpretation Notes",
        "",
        "- Server banners describe observed response headers "
        "and do not prove physical origin.",
        "- Content or favicon changes indicate observed changes "
        "between scans and do not automatically indicate "
        "infrastructure migration.",
        "- Wallet matches are graph-correlation signals and do "
        "not prove ownership.",
        "- Certificate Transparency matches are infrastructure "
        "correlation clues requiring independent review.",
        "- Confidence values describe the strength of recorded "
        "signals, not the probability of identifying a "
        "real-world actor.",
        "",
    ])

    con.close()

    Path(out_path).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return out_path
