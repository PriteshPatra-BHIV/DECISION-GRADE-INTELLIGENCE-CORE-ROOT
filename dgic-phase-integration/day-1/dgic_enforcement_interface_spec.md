# DGIC ↔ Enforcement Interface Specification v1

## Contract Overview

**Producer**: DGIC Core (Epistemic Engine)  
**Consumer**: Rajaryan (Enforcement Layer)  
**Direction**: Unidirectional (DGIC → Enforcement)  
**Mutation Guarantee**: Enforcement CANNOT mutate DGIC envelope

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

### Field Semantics

| Field | Type | Semantics | Enforcement Constraint |
|-------|------|-----------|----------------------|
| `epistemic_state` | enum | Knowledge state | Cannot be modified |
| `confidence` | float | Certainty measure | Cannot be modified |
| `contradiction_flag` | bool | Contradiction detected | Cannot be modified |
| `evidence_hash` | string | Evidence integrity | Cannot be modified |
| `collapse_flag` | bool | Collapse occurred | Cannot be modified |
| `entropy_score` | number | System entropy | Cannot be modified |

---

## Enforcement Adapter Constraints

### Read-Only Access
```python
# ALLOWED: Read envelope fields
risk_score = envelope["confidence"] * 0.5

# FORBIDDEN: Modify envelope
envelope["confidence"] = 0.9  # ❌ VIOLATION
```

### Deterministic Computation
- Enforcement must compute risk scores deterministically
- Same input envelope → same risk score (always)
- No probabilistic shortcuts

### Ambiguity Handling
- If `epistemic_state == "AMBIGUOUS"`, enforcement MUST NOT collapse to certainty
- Ambiguity is valid state, not error condition
- Enforcement must abstain or escalate, never force resolution

### Contradiction Propagation
- If `contradiction_flag == true`, enforcement MUST escalate
- Contradictions cannot be silently ignored
- Enforcement must log contradiction with evidence hash

---

## Emission Protocol

1. DGIC generates epistemic snapshot
2. Runtime schema guard validates envelope
3. Integrity hash computed: `SHA256(canonical_json(envelope))`
4. Sealed envelope emitted: `{envelope, integrity_hash, sealed: true}`
5. Enforcement receives sealed envelope
6. Enforcement verifies integrity hash before processing
7. Enforcement reads fields (no mutation)
8. Enforcement emits risk score (separate output)

---

## Failure Modes

### Invalid Envelope
- **Trigger**: Schema validation fails
- **Action**: Fail-closed, reject envelope
- **Log**: Validation error with evidence hash

### Hash Mismatch
- **Trigger**: Integrity hash verification fails
- **Action**: Fail-closed, reject envelope
- **Log**: Tampering detected

### Enforcement Mutation Attempt
- **Trigger**: Enforcement modifies envelope field
- **Action**: Detect via replay verification
- **Log**: Privilege escalation attempt

---

## Testing Requirements

- [ ] Envelope schema validation (100 iterations)
- [ ] Integrity hash verification (100 iterations)
- [ ] Ambiguity preservation (50 iterations)
- [ ] Contradiction propagation (50 iterations)
- [ ] Enforcement read-only access (100 iterations)
- [ ] Deterministic risk scoring (1000 iterations)

---

## Version Control

- **Version**: v1
- **Locked**: Yes
- **Modification**: Requires cross-layer consensus
