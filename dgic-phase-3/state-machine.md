# Deterministic Epistemic State Machine

## Purpose

This document formally defines the executable epistemic
state machine used in Phase 3 sealing.

This state machine is deterministic, irreversible,
and cryptographically auditable.

---

## States

The system operates in exactly four states:

- Known
- Inferred
- Ambiguous
- Unknown

No additional states are permitted.

---

## Deterministic Rule

Given:
- Current state
- Target state
- Evidence flag
- Collapse flag

The resulting transition is deterministic.

No randomness is allowed.
No probabilistic resolution is permitted.

---

## Transition Enforcement

Transitions are validated against:

- transition-matrix.json
- Evidence requirements
- Collapse justification requirements

Illegal transitions raise runtime exceptions.

---

## Irreversibility

Each valid transition produces:

- Unique transition ID
- Timestamp
- Hash of event
- Chained previous hash reference

Transitions are append-only.
No mutation is allowed.

---

## Hash Chain Structure

Each event contains:

previous_hash → event_data → event_hash

This forms a cryptographic chain.

If any historical event changes,
all downstream hashes break.

---

## Deterministic Replay

Replaying the journal must:

- Reproduce identical state sequence
- Reproduce identical final hash
- Fail if any mutation occurred

Replay integrity is required for system sealing.

---

## Epistemic Guarantee

The state machine guarantees:

- Illegal promotions are impossible
- Collapse cannot occur silently
- Ambiguity remains auditable
- Unknown cannot auto-promote

The state machine is the enforcement layer
of epistemic discipline.
