# Architecture

```text
Datasets + Authorized Observations
              |
              v
       Ingestion / Normalization
              |
              v
       Intelligence Data Store
              |
       +------+------+
       |             |
       v             v
Infrastructure   Relationship
Observation      Graph
       |             |
       v             v
Fingerprint +   Onion <-> ID
Evidence        correlation
       |             |
       +------+------+
              |
              v
      Temporal Correlation
              |
              v
       Confidence / Evidence
              |
              v
        Analyst Dashboard
```

## Infrastructure observation

An observation is immutable evidence tied to a target and timestamp. Raw response material should be minimized and sensitive values redacted before persistence.

## Evidence model

Each indicator should carry:

- indicator type
- observed value or safe fingerprint
- observation timestamp
- source
- confidence
- supporting evidence

The system should distinguish an **observation** from an **attribution claim**. Infrastructure similarity is evidence for correlation, not proof of actor identity.
