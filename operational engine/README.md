# DGIC Operational Reasoning Engine
### Phase 1 — Full Pipeline Implementation

A deterministic, auditable, and traceable decision engine built for real-world operational environments including Marine Intelligence, Military Decision Systems, and Agriculture Intelligence (AIAIC).

---

## Overview

This engine takes multi-signal inputs, runs them through a structured reasoning pipeline, and produces enforceable, fully traceable decisions. Every execution is hashed, logged, and replayable.

---

## Pipeline Flow

```
Input Signals
     │
     ▼
validate_signals()         — reject invalid/malformed signals, sanitize input
     │
     ▼
apply_temporal_ordering()  — sort signals by timestamp (forward-only)
     │
     ▼
evolve_states()            — assign base confidence per signal type, apply noise
     │
     ▼
resolve_interference()     — suppress SAFE states overridden by prior THREAT states
     │
     ▼
collapse_states()          — select dominant state by priority → confidence → timestamp
     │
     ▼
generate_decision()        — produce final decision contract
     │
     ▼
log_execution()            — write to replay ledger with SHA-256 hash
     │
     ▼
Output Decision Contract
```

---

## Input Schema

```json
{
  "signals": [
    {
      "id": "S1",
      "type": "THREAT | SAFE | UNKNOWN",
      "priority": 1,
      "timestamp": 1,
      "noise": 0.0
    }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `id` | Yes | Unique signal identifier |
| `type` | Yes | Must be `THREAT`, `SAFE`, or `UNKNOWN` |
| `priority` | No | Integer. Higher = stronger dominance. Default: `0` |
| `timestamp` | No | Integer. Used for temporal ordering. Default: `0` |
| `noise` | No | Float 0–1. Values above `0.5` halve confidence |

---

## Output Decision Contract

```json
{
  "execution_id": "uuid",
  "execution_hash": "sha256",
  "decision": "ESCALATE | PROCEED | HOLD | REQUEST_MORE_DATA",
  "confidence": 0.6,
  "epistemic_state": "THREAT | SAFE | UNKNOWN | AMBIGUOUS",
  "reason_trace": [],
  "collapse_trigger": "dominance | none"
}
```

| Decision | Trigger Condition |
|---|---|
| `ESCALATE` | Dominant state is `THREAT` |
| `PROCEED` | Dominant state is `SAFE` |
| `HOLD` | Confidence below `0.3` threshold |
| `REQUEST_MORE_DATA` | Ambiguity detected (confidence gap < `0.05`) or `UNKNOWN` state |

---

## API Functions

### `api_run_reasoning(input_data)`
Runs the full reasoning pipeline. Returns a structured response.

```python
response = api_run_reasoning({
    "signals": [
        {"id": "S1", "type": "THREAT", "priority": 1, "timestamp": 1},
        {"id": "S2", "type": "SAFE",   "priority": 2, "timestamp": 2}
    ]
})
# {"status": "success", "data": { ...decision contract... }}
```

### `get_replay_trace(execution_id)`
Retrieves the full execution record from the replay ledger.

```python
record = get_replay_trace("uuid")
# Returns full record including input, states, collapse info, decision, and hash
# Returns None if not found
```

---

## API Output Examples

### Scenario 1 — Normal
Single SAFE signal with higher priority than THREAT.
```json
{
  "status": "success",
  "data": {
    "decision": "PROCEED",
    "confidence": 0.6,
    "epistemic_state": "SAFE",
    "collapse_trigger": "dominance"
  }
}
```

### Scenario 2 — Conflict
THREAT and SAFE at equal priority. THREAT wins by confidence.
```json
{
  "status": "success",
  "data": {
    "decision": "ESCALATE",
    "confidence": 0.8,
    "epistemic_state": "THREAT",
    "collapse_trigger": "dominance"
  }
}
```

### Scenario 3 — Failure
Missing `signals` key in input.
```json
{
  "status": "error",
  "message": "Missing 'signals' in input"
}
```

---

## Running the Engine

```bash
python phase1_pipeline.py
```

This runs all 3 API scenarios, full validation, 1000-run stress test, and a 5-node distributed simulation.

---

## Constants

| Constant | Value | Purpose |
|---|---|---|
| `HOLD_CONFIDENCE_THRESHOLD` | `0.3` | Minimum confidence before HOLD is issued |
| `AMBIGUITY_THRESHOLD` | `0.05` | Max confidence gap before ambiguity is declared |
| `VALID_SIGNAL_TYPES` | `THREAT, SAFE, UNKNOWN` | Accepted signal types |
| `VALID_DECISIONS` | `ESCALATE, PROCEED, HOLD, REQUEST_MORE_DATA` | Valid output decisions |

---

## Integration

| Team | Role | Hook |
|---|---|---|
| Rajaryan Verma | Enforcement Engine | Consumes `api_run_reasoning()` output |
| Aakanksha Parab | AI Being Orchestrator | Triggers `run_reasoning_pipeline()` across agents |
| Vinayak Tiwari | Testing & Validation | Uses `run_full_validation()`, `stress_test()`, `get_replay_trace()` |
| Akash | Functional Testing | Validates `api_run_reasoning()` and `api_get_replay()` |

---

## Security

- All signal `id` and `type` fields are sanitized with `html.escape()` before entering trace strings
- Internal stack traces are never exposed through API responses
- Ledger reads/writes are protected by a `threading.Lock` for concurrent safety
- Input validation raises typed exceptions (`TypeError`, `ValueError`) caught at the API boundary
