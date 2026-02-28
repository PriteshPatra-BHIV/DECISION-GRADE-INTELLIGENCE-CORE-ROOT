# Temporal Model — Intelligence Core

## Purpose

This document formalizes how time is represented
inside the Decision-Grade Intelligence Core.

The system must:

- Respect forward-only time
- Prevent retroactive mutation
- Preserve causal ordering
- Remain replay-consistent

Time is treated as a structural dimension,
not an assumption.

---

## Temporal States

Each signal exists in exactly one temporal state:

1. Pre-Observation
2. Observed
3. Collapsed
4. Archived

No signal may skip states.
No signal may move backward.

---

## 1. Pre-Observation

Signal exists externally.
Not yet ingested.
No epistemic impact.

Cannot affect system state.

---

## 2. Observed

Signal ingested.
Epistemic state assigned.
No irreversible certainty yet.

Observed does not imply resolved.

---

## 3. Collapsed

Ambiguity resolved via evidence.
Certainty formally logged.
Hash-chained in ledger.

Irreversible transition.

---

## 4. Archived

Signal preserved for history.
No longer active in reasoning.
Replay-visible.

Cannot re-enter Observed.

---

## Allowed Temporal Transitions

Pre-Observation → Observed  
Observed → Collapsed  
Observed → Archived  
Collapsed → Archived  

---

## Forbidden Transitions

Archived → Observed  
Collapsed → Observed  
Archived → Collapsed  
Any backward movement  

---

## Temporal Integrity Principle

Time flows forward only.

No signal may:

- Re-enter prior temporal state
- Rewrite historical timestamp
- Modify prior collapse event

Temporal discipline protects epistemic integrity.