# Replay Hash Proof

## Purpose

This document explains why deterministic replay
is cryptographically provable in Phase 3.

Runtime proof replaces documentation-only guarantees.

---

## Hashing Model

Each transition event is serialized using:

JSON (sorted keys)

Then hashed using:

SHA-256

event_hash = SHA-256(serialized_event_without_event_hash)

Each event stores:

previous_hash → linking to prior event_hash

This creates a forward-linked cryptographic chain.

---

## Determinism Condition

For replay to succeed:

1. Transition matrix must be identical.
2. Journal must be identical.
3. Serialization order must be stable.
4. Hash function must be deterministic.
5. No nondeterministic timestamps in replay verification.

If all conditions hold,
replay produces identical state sequence and identical final hash.

---

## Mutation Detection

If any of the following occur:

- A journal entry is modified
- A journal entry is deleted
- A journal entry is reordered
- A field value changes
- Evidence flags change

Then:

- Hash recomputation fails
OR
- Hash chain continuity fails

Replay engine raises exception.

---

## Replay Algorithm

For each journal entry:

1. Verify previous_hash matches last computed hash.
2. Remove event_hash.
3. Recompute SHA-256.
4. Compare to stored event_hash.
5. Continue chain.

Final hash must match across repeated runs.

---

## 1000-Run Stability Proof

Replay harness executes 1000 replays.

If any run produces:

- Different state sequence
- Different final hash

System fails determinism compliance.

Passing 1000-run replay test proves:

- No hidden mutation
- No nondeterministic state evolution
- No implicit randomness

---

## Cryptographic Sealing Insight

The system is sealed because:

- History cannot change undetected.
- Certainty cannot be injected retroactively.
- Collapse cannot be erased.
- State cannot silently mutate.

Hash chaining converts epistemic discipline
into runtime enforceable integrity.
