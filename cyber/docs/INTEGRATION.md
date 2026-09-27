# Integration Handoff — Cybersecurity Infrastructure Module

## 1. Purpose

This module provides authorized/controlled Tor onion-service infrastructure intelligence for the SIH platform.

It extracts infrastructure fingerprints, detects security-relevant indicators, classifies observed threats, performs infrastructure correlation, tracks temporal changes, and produces evidence-backed outputs.

The module supports attribution analysis but does not make definitive deanonymization or identity claims.

---

## 2. Module Outputs

The module produces:

- Onion-service observation metadata
- HTTP/service information
- Server/banner fingerprints
- Body SHA-256 fingerprint
- Favicon fingerprint
- TLS certificate SHA-256 fingerprint
- Exposed service/path indicators
- Threat classification labels
- Wallet indicators
- Infrastructure correlation clues
- Temporal/change analysis
- Evidence and confidence values
- JSON/CSV/Markdown investigator reports

---

## 3. Common Indicator Schema

Backend and ML systems should use the following normalized fields:

target_id
onion_address
timestamp
indicator_type
indicator_value
source
evidence
candidate_match
confidence
severity
first_seen
last_seen

Confidence represents the strength of an observed correlation or classification signal. It must not be interpreted as proof of attribution.

---

## 4. Infrastructure Observation

Example:

{
  "http_status": 200,
  "server": "Apache/2.4.68 (Debian)",
  "content_type": "text/html",
  "content_length": 87,
  "page_title": null,
  "body_sha256": "...",
  "favicon_sha256": null,
  "tls_cert_sha256": null
}

---

## 5. Security Indicators

Example:

{
  "indicator_type": "EXPOSED_SERVER_STATUS",
  "severity": "high",
  "confidence": 0.90,
  "evidence": "HTTP 200 response from /server-status"
}

Other indicators may include:

EXPOSED_SERVER_STATUS
SERVER_BANNER
DEFAULT_WEB_PAGE
EXPOSED_PATH
TLS_CERTIFICATE_MATCH

---

## 6. Threat Classification

Current baseline categories:

credential_theft
data_theft
malware
fraud
hacking_services
drugs
weapons

The current classifier is rule-based and should be treated as a baseline for comparison with the ML model.

The Agora benchmark is category-hit coverage, not ML accuracy or forensic ground truth.

---

## 7. ML Integration

The ML team can use the following as model features:

### Infrastructure features

server_banner
body_sha256
favicon_sha256
tls_cert_sha256
http_status
content_type
content_length

### Security features

server_status_exposed
exposed_path_count
default_page_detected
tls_present
certificate_match

### Temporal features

observation_count
first_seen
last_seen
server_changed
body_changed
favicon_changed
availability_changed
migration_signal

### Threat features

credential_theft
data_theft
malware
fraud
hacking_services
drugs
weapons

The ML model should return predicted categories and confidence scores without making definitive attribution claims.

---

## 8. Backend Integration

The backend should:

1. Receive authorized observation requests.
2. Store observations.
3. Store indicators separately where possible.
4. Preserve evidence and confidence.
5. Store first_seen and last_seen timestamps.
6. Expose structured JSON through the backend API.
7. Prevent unauthorized probing.
8. Validate all input.
9. Keep sensitive keys, credentials and raw datasets out of API responses.

Recommended logical entities:

Observation
Indicator
ThreatClassification
InfrastructureCorrelation
TemporalEvent
WalletIndicator

---

## 9. Frontend Integration

The frontend can display:

### Target Overview

Target
Scan time
HTTP status
Server
Content type
First seen
Last seen

### Infrastructure

Server fingerprint
Body fingerprint
Favicon fingerprint
TLS fingerprint

### Security Findings

Indicator type
Severity
Confidence
Evidence

### Threat Classification

Category
Confidence

### Correlation

Candidate infrastructure
Correlation type
Evidence
Confidence

### Timeline

First seen
Last seen
Observed changes
Migration signals

Correlation should be displayed as a potential/candidate relationship, not confirmed attribution.

---

## 10. Temporal Analysis

Repeated observations of the same authorized target are compared for:

- Server banner changes
- Body fingerprint changes
- Favicon changes
- Availability changes
- Possible migration signals

A content change alone must not be treated as infrastructure migration.

---

## 11. Infrastructure Correlation

TLS certificate information can be correlated with public Certificate Transparency data where applicable.

A certificate match is a correlation clue, not proof that the identified clearnet infrastructure is the origin server or belongs to a particular actor.

Current correlation confidence should therefore be interpreted conservatively.

---

## 12. Wallet Indicators

Supported wallet/address categories include:

bitcoin_legacy
bitcoin_segwit
ethereum
monero
litecoin

Wallet extraction identifies observed indicators only.

An observed wallet address does not prove ownership or attribution.

---

## 13. Evidence Model

Every important analytical result should retain:

- What was observed
- When it was observed
- Where it came from
- Which indicator generated it
- Evidence supporting the result
- Confidence
- Candidate relationship, if applicable

Evidence should be treated as a first-class object when building the final graph.

---

## 14. Recommended System Flow

Authorized Onion Target
        |
        v
Infrastructure Probe
        |
        v
Fingerprint Extraction
        |
        v
Misconfiguration Detection
        |
        v
Threat Classification
        |
        v
Infrastructure Correlation
        |
        v
Temporal Analysis
        |
        v
Evidence + Confidence
        |
        +-----------> Backend
        |
        +-----------> ML
        |
        +-----------> Frontend
        |
        v
Investigator Dashboard / Report

---

## 15. Important Scope

This module is designed for authorized cybersecurity research and controlled testing.

Outputs are intended to provide:

- Infrastructure intelligence
- Candidate relationships
- Evidence
- Correlation signals
- Confidence scores
- Threat intelligence

The system must not represent these signals as guaranteed identity attribution or definitive deanonymization.

---

## 16. Current Implementation Status

Completed:

- Tor v3 validation
- Onion probing
- Infrastructure fingerprinting
- Misconfiguration detection
- TLS fingerprinting
- Infrastructure correlation
- Threat classification baseline
- Wallet extraction/correlation
- Temporal analysis
- Investigator reports
- JSON/CSV/Markdown export
- Security hardening
- Controlled Docker/Tor testing

Next integration work:

Backend + ML + Frontend connection using the common structured output defined above.
