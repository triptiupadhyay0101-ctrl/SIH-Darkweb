# Methodology

## 1. Observe

Collect approved observations with a timestamp and source identifier.

## 2. Normalize

Convert heterogeneous source records into common entities: `service`, `observation`, `indicator`, `identifier`, `category`, and `source`.

## 3. Fingerprint

Generate reproducible, privacy-conscious fingerprints from server metadata, headers, page title, body content and favicon data where available.

## 4. Detect

Flag observable conditions such as exposed diagnostic endpoints, unexpected/default service characteristics and fingerprint changes.

## 5. Correlate

Compare observations across time and across services. Combine infrastructure evidence with relationship-graph context.

## 6. Score

Produce an evidence-backed confidence score. The score must not be represented as certainty of real-world identity.

## 7. Explain

Every score should be accompanied by the indicators that contributed to it, their timestamps and their sources.
