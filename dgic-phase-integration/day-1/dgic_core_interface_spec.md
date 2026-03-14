# DGIC ↔ Core Routing Interface Specification v1

## Contract Overview

**Producer**: DGIC Core (Epistemic Engine)  
**Consumer**: Aakanksha (Core Orchestration & Routing)  
**Direction**: Unidirectional (DGIC → Core)  
**Mutation Guarantee**: Core CANNOT mutate DGIC envelope  
**Authority Guarantee**: Intelligence signals CANNOT become authority signals

---

## Envelope Schema

All DGIC outputs conform to:

```json
{
  "epistemic_state": "CERTAIN|AMBIGUOUS|CONTRADICTORY",
  "confidence": 0.0-1.0,
  "contradiction_flag": boolean,
  "evidence_hash": "sha256_hex_string",
  "collapse_flag": boolean,
  "entropy_score": number >= 0
}
```

### Authority Semantics

**CRITICAL**: DGIC envelopes are **intelligence signals**, NOT authority signals.

- Intelligence: "Here's what we know and don't know"
- Authority: "Here's what you must do"

Core MUST NOT convert intelligence → authority.

---

## Core Routing Constraints

### Schema Validation Enforcement
```python
# REQUIRED: Validate envelope before routing
if not validate_schema(envelope):
    reject_envelope()  # Fail-closed

# REQUIRED: Verify integrity hash
if not verify_hash(envelope):
    reject_envelope()  # Fail-closed
```

### Version Mismatch Rejection
```python
# REQUIRED: Reject mismatched schema versions
if envelope_version != DGIC_SCHEMA_VERSION:
    reject_envelope()  # Fail-closed
```

### Authority Field Protection
```python
# FORBIDDEN: Modify authority fields
envelope["epistemic_state"] = "CERTAIN"  # ❌ VIOLATION
envelope["confidence"] = 1.0  # ❌ VIOLATION

# FORBIDDEN: Inject authority into envelope
envelope["decision_mandate"] = "EXECUTE"  # ❌ VIOLATION
```

### Routing Lineage Logging
```python
# REQUIRED: Log routing path with timestamps
routing_log = {
    "source": "DGIC",
    "timestamp": iso8601_now(),
    "envelope_hash": envelope_hash,
    "routing_path": ["DGIC", "Core", "Enforcement"],
    "validation_status": "PASSED"
}
```

---

## Routing Protocol

1. DGIC emits sealed envelope with integrity hash
2. Core receives envelope
3. Core validates schema (reject if invalid)
4. Core verifies integrity hash (reject if mismatch)
5. Core checks version compatibility (reject if mismatch)
6. Core logs routing lineage
7. Core routes envelope to downstream consumers
8. Core NEVER modifies envelope fields
9. Core NEVER converts intelligence → authority

---

## Ambiguity Handling

### Core MUST NOT Collapse Ambiguity
```python
# FORBIDDEN: Force certainty
if envelope["epistemic_state"] == "AMBIGUOUS":
    envelope["epistemic_state"] = "CERTAIN"  # ❌ VIOLATION

# REQUIRED: Preserve ambiguity
if envelope["epistemic_state"] == "AMBIGUOUS":
    route_to_escalation_handler()  # ✅ CORRECT
```

### Contradiction Handling
```python
# REQUIRED: Escalate contradictions
if envelope["contradiction_flag"]:
    route_to_contradiction_handler()  # ✅ CORRECT
    log_contradiction(envelope["evidence_hash"])
```

---

## Failure Modes

### Schema Validation Failure
- **Trigger**: Envelope doesn't match schema
- **Action**: Fail-closed, reject envelope
- **Log**: Validation error with evidence hash

### Hash Verification Failure
- **Trigger**: Integrity hash mismatch
- **Action**: Fail-closed, reject envelope
- **Log**: Tampering detected

### Version Mismatch
- **Trigger**: Envelope version ≠ Core version
- **Action**: Fail-closed, reject envelope
- **Log**: Version incompatibility

### Authority Mutation Attempt
- **Trigger**: Core modifies authority fields
- **Action**: Detect via replay verification
- **Log**: Privilege escalation attempt

---

## Testing Requirements

- [ ] Schema validation enforcement (100 iterations)
- [ ] Integrity hash verification (100 iterations)
- [ ] Version mismatch rejection (50 iterations)
- [ ] Authority field immutability (100 iterations)
- [ ] Routing lineage logging (100 iterations)
- [ ] Ambiguity preservation (50 iterations)
- [ ] Contradiction escalation (50 iterations)

---

## Version Control

- **Version**: v1
- **Locked**: Yes
- **Modification**: Requires cross-layer consensus
