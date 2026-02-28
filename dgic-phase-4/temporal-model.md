# Temporal Model — Intelligence Core

## Purpose

This document formalizes time and state evolution
inside the Decision-Grade Intelligence Core.

Time is treated as a structural dimension,
not an implicit ordering assumption.

---

## Temporal States

Each epistemic signal exists in exactly one temporal state:

1. Pre-Observation
2. Observed
3. Collapsed
4. Archived

No signal may skip a temporal state.

---

## 1. Pre-Observation

Definition:
- Signal exists externally.
- Not yet ingested.
- No epistemic state assigned.

Properties:
- Not part of system history.
- Cannot affect downstream outputs.

---

## 2. Observed

Definition:
- Signal ingested.
- Assigned epistemic state.
- No collapse executed.

Properties:
- Can contribute to ambiguity.
- Cannot produce irreversible certainty.

Observed does not imply resolved.

---

## 3. Collapsed

Definition:
- Ambiguity resolved via formal collapse.
- New evidence validated.
- Collapse logged in ledger.

Properties:
- Irreversible transition.
- Must include evidence reference.
- Must include collapse justification.

Collapse produces certainty but preserves prior history.

---

## 4. Archived

Definition:
- Signal no longer active in reasoning.
- Preserved for audit and replay.

Properties:
- Cannot re-enter Observed.
- Cannot alter current state.
- Must remain replay-reconstructable.

Archival is temporal sealing.

---

## Temporal Transition Rules

Allowed progression:

Pre-Observation → Observed  
Observed → Collapsed  
Observed → Archived  
Collapsed → Archived  

Forbidden:

Archived → Observed  
Collapsed → Observed  
Any retroactive rewrite of prior temporal state  

---

## Temporal Integrity Principle

Time flows forward only.

No signal may:
- Re-enter earlier temporal state.
- Modify past collapse event.
- Rewrite prior ambiguity.

Temporal coherence is mandatory.

---

## System Insight

Epistemic state answers:
"What do we know?"

Temporal state answers:
"When did we know it and can it change?"

Both dimensions must remain consistent.
