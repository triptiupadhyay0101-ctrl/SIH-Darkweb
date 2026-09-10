# Methodology — Infrastructure Intelligence Collection

## 1. Test environment

A Docker container (`darkweb-lab`) runs Debian + Apache + Tor, with Apache's
`mod_status` deliberately enabled and exposed at `/server-status` without
authentication. This simulates a real-world misconfigured onion service and
serves as ground truth for validating detection logic before it is applied
to any authorized real-world target.

## 2. Observation pipeline

1. Connect to the target `.onion` address via a local Tor SOCKS5 proxy
   (`127.0.0.1:9050`).
2. Fetch `/` — record HTTP status, `Server` header, page title, and a
   SHA-256 hash of the response body.
3. Fetch `/favicon.ico` — record its SHA-256 hash (usable for cross-referencing
   against clearnet favicon databases such as Shodan's `http.favicon.hash`).
4. Run a battery of GET requests against nine known-sensitive paths
   (`/server-status`, `/.git/config`, `/.env`, etc.), each with a
   content-match rule to reduce false positives from custom 200-OK error pages.
5. Emit one indicator record per positive finding, each carrying a
   `severity`, `confidence`, and human-readable `evidence` string.

## 3. Storage

All observations and indicators are persisted to a local SQLite database
using parameterized queries exclusively (no string-built SQL), satisfying
the project's own secure-coding requirement (SIH PS item 5).

## 4. Data quality

Content-matching (not just status-code checks) is used wherever a path's
positive/negative response can be textually distinguished, to avoid the
common false-positive of servers returning HTTP 200 for every path
(soft-404 behavior).

## 5. Real datasets integrated

- **Bipartite onion↔identifier graph** (139,356 nodes / 248,791 edges) —
  imported via `ingest-graphml`, gives a real actor-relationship graph
  (onion services linked to PGP keys, wallets, Telegram handles, etc.)
  for the backend/AI correlation layer to build on.
- **Tor Project hidserv-dir metrics** — imported via `ingest-tor-metrics`,
  gives a network-wide daily onion-count baseline for temporal-context
  analysis (Module 4 concept).

## 6. Implemented extensions

- TLS certificate SHA-256 fingerprint extraction is implemented for
  HTTPS observations. Where a certificate is available, its fingerprint
  can be used as an infrastructure-correlation clue.
- Certificate Transparency correlation through crt.sh is implemented.
  A certificate match is treated as a correlation signal, not proof of
  origin ownership or attribution.
- Favicon fingerprint extraction is implemented for HTTP observations
  and can support future cross-infrastructure correlation.
- Wallet extraction and correlation support is implemented for
  Bitcoin, Ethereum, Monero, and Litecoin indicators.
- Temporal analysis compares repeated observations for server-banner,
  body-fingerprint, favicon, and availability changes. Content changes
  alone are not treated as infrastructure migration.
- Security hardening includes Tor v3 validation, bounded response
  processing, validated configuration values, request timeouts,
  disabled redirects, and configurable batch delays.
- The module produces structured JSON, CSV, and Markdown investigator
  reports for downstream backend, ML, graph, and frontend integration.
