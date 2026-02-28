# Collapse Ledger Specification — Temporal Irreversibility

## Purpose

This document formalizes the Collapse Ledger,
extending the Phase 3 journal into a temporally coherent,
causally sealed irreversible ledger.

The ledger enforces:

- Irreversibility
- Temporal coherence
- Collapse traceability
- Ambiguity archival

---

## Ledger Scope

The Collapse Ledger records:

- All epistemic state transitions
- All temporal state transitions
- All collapse events
- All archival events

No state mutation may occur without ledger entry.

---

## Ledger Entry Requirements

Each ledger entry must include:

- transition_id
- event_timestamp (system ingestion time)
- signal_timestamp (external origin time)
- previous_epistemic_state
- new_epistemic_state
- previous_temporal_state
- new_temporal_state
- evidence_reference (if applicable)
- collapse_flag
- previous_hash
- event_hash

All fields are mandatory.

---

## Temporal Consistency Rule

For any ledger entry:

event_timestamp must be strictly greater than
the previous ledger entry timestamp.

Signal timestamps may be earlier,
but ledger insertion order must never rewrite history.

---

## Collapse Irreversibility Rule

If:

previous_epistemic_state == "Ambiguous"
AND new_epistemic_state == "Known"

Then:

- collapse_flag must be True
- evidence_reference must exist
- ledger entry must be appended
- prior ambiguity must remain reconstructable

Collapse cannot be undone.

---

## Ambiguity Archival Requirement

When collapse occurs:

- Pre-collapse ambiguity must be archived.
- Archived state must remain replay-accessible.
- Ambiguity cannot be deleted.

Certainty reduces runtime ambiguity,
but never erases history.

---

## Ledger Immutability Rule

Ledger must be:

- Append-only
- Cryptographically chained
- Replay-verifiable
- Mutation-detectable

Any change invalidates deterministic replay.

---

## No Retroactive Insertion Rule

The system must never:

- Insert entries into prior position
- Modify prior timestamps
- Reorder events
- Replace prior hash

Ledger order defines causal history.

---

## Structural Insight

The Collapse Ledger encodes:

Time + State + Evidence + Hash

This binds epistemic evolution
to irreversible temporal structure.

Irreversibility is no longer conceptual.
It is structural.
