# DGIC Runtime API

## Overview

The **DGIC Runtime API** exposes the **Decision Grade Intelligence Core (DGIC)** as a reasoning service within the **BHIV ecosystem**.

External systems such as **InsightBridge**, the **Enforcement Layer**, and the **AI Being Orchestrator** can submit signals to DGIC and receive **deterministic epistemic evaluations**.

DGIC **does not execute decisions**. It only produces **epistemic intelligence**.

---

## Endpoint

```
POST /dgic/evaluate
```

---

## Input Schema

Request body fields:

| Field | Type | Description |
|------|------|-------------|
| `signals` | list | Input signals from external systems |
| `context` | object | Additional contextual information |
| `source_system` | string | Identifier of the system sending the request |
| `prior_state` | object | Previous epistemic state (if available) |

Valid signal types: `THREAT`, `CONTRADICTION`, `ANOMALY`, `CORRUPTION`

Signal `value` must be between `0.0` and `1.0` (inclusive). Values outside this range are rejected with HTTP 422.

### Example Request

```json
{
  "signals": [
    {
      "signal_id": "S1",
      "type": "THREAT",
      "value": 0.6
    }
  ],
  "context": {},
  "source_system": "InsightBridge",
  "prior_state": {}
}
```

---

## Output Schema

DGIC returns a **structured epistemic envelope** containing the following fields:

| Field | Type | Description |
|------|------|-------------|
| `epistemic_state` | string | Evaluated epistemic classification (`CERTAIN` or `AMBIGUOUS`) |
| `confidence` | float | Confidence score for the evaluation |
| `contradiction_flag` | boolean | Indicates conflicting signals |
| `entropy_score` | float | Uncertainty level of the reasoning state |
| `collapse_flag` | boolean | Indicates epistemic collapse condition |
| `trace_hash` | string | SHA256 hash for reasoning trace verification |

### Example Response

```json
{
  "epistemic_state": "AMBIGUOUS",
  "confidence": 0.6,
  "contradiction_flag": false,
  "entropy_score": 0.4,
  "collapse_flag": false,
  "trace_hash": "abc123..."
}
```

---

## Design Guarantees

The runtime API maintains the following guarantees:

- Deterministic reasoning
- Immutable epistemic outputs
- Replay verifiability
- Explicit uncertainty preservation
- Input bounds enforcement (forced certainty attack prevention)

DGIC informs decisions but never executes them.