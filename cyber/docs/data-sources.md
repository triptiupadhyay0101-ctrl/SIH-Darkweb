# Data Sources and Availability

| Source | Available | Primary use | Important limitation |
|---|---:|---|---|
| DIZZY domains | Yes | domain category/context | Public onion identifiers are hashed |
| DIZZY pages | Yes | historical pages/paths | Not a full infrastructure fingerprint dataset |
| DIZZY Bitcoin | Yes | onion ↔ wallet context | Relationship data, not infrastructure metadata |
| Bipartite Tor Domains ↔ IDs | Yes | onion ↔ identifier graph | Treat identifiers as sensitive and redact in demos |
| Tor Metrics CSV | Yes | network-level temporal baseline | Aggregate, not target-level evidence |
| CIRCL AIL | Available | screenshot/content correlation | Visual data, not HTTP/TLS telemetry |
| Controlled Docker/Tor lab | Yes | ground-truth infrastructure observations | Represents the lab, not arbitrary real services |
| Historical HTTP/TLS/fingerprint dataset | Not yet required | external validation | Can be added later if an authorized dataset is obtained |
