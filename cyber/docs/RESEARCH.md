# Dark-Web & Tor Research Notes

## Tor and onion services

Tor routes traffic through three relays (guard, middle, exit) to hide a
client's origin. Onion services go further: they never use an exit node.
Both the client and the service build circuits to a randomly chosen
rendezvous point, meeting there without either party learning the other's
IP address.

A v3 onion address (current standard, 56 base32 characters) is derived
directly from the service's ed25519 public key — there is no central
DNS-like registry. The service periodically publishes a signed descriptor
(containing its introduction points) to a rotating set of HSDir (Hidden
Service Directory) nodes in Tor's distributed hash table, so clients can
discover how to reach it.

## How threat actors use hidden services

- IP concealment is the core motivation — a marketplace/forum operator
  never exposes a real server IP.
- Consistent identity for trust: marketplaces need reputation systems, so
  vendors keep a stable handle plus PGP key even while hiding
  infrastructure. This consistency is exactly what makes cross-platform
  linking possible.
- Rebranding after takedown or exit scam: operators frequently stand up a
  new onion address reusing old server images or panel code in a hurry,
  which is why misconfigurations are common right after a migration.

## Common infrastructure clues detected by this module

| Clue | Why it leaks information |
|---|---|
| Exposed /server-status, /server-info | Reveals internal IP, other vhosts, live traffic |
| Reused TLS certificate | Certificate Transparency logs make clearnet reuse public and permanent |
| Default/unmodified banners | Confirms software stack + version |
| Exposed .git, .env, backup files | Direct leak of source code, credentials, structure |
| Favicon/body hash reuse | Same static assets often redeployed across operator infrastructure |

## Descriptor inconsistencies (known gap)

The PS also asks for descriptor inconsistencies as an infrastructure clue.
This refers to anomalies in how an onion service's introduction points are
published to HSDir nodes -- for example, two onion addresses whose
descriptors are consistently published via the same narrow set of relays.
Implementing this requires parsing Tor's live network consensus directly
via the Tor control protocol (the `stem` library), which is a materially
heavier task than HTTP-level probing. This is flagged as a known gap and a
concrete next step, not silently skipped.

## Key sources

- Buitrago Lopez et al., "Updated exploration of the Tor network:
  advertising, availability and protocols of onion services", Wireless
  Networks (2024) -- 54,602 onions tracked over 6 months; HTTP dominant
  at 99.75%, SSH second at 4.95%; informed prioritizing HTTP-based checks.
- de-Marcos et al., bipartite onion-identifier graph dataset (used in this
  module's ingest-graphml command).
- Jin et al., "Sharing cyber threat intelligence: Does it really help?",
  NDSS 2024 -- informed the confidence-scoring approach.
