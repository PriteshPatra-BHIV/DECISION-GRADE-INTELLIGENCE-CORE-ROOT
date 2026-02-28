# Temporal Conflict Handling — Multi-Signal Order Integrity

## Purpose

This document defines how the Intelligence Core
handles signals that arrive:

- Out of chronological order
- With conflicting timestamps
- After prior collapse has occurred

The system must preserve causal integrity
without retroactive rewriting.

---

## Problem Definition

Signals have two times:

1. signal_timestamp — when event occurred externally
2. event_timestamp — when system ingested the signal

These may not match.

Out-of-order arrival is expected.

---

## Core Rule

Ledger order is determined by event_timestamp,
not signal_timestamp.

Historical ordering is defined by ingestion sequence.

No retroactive insertion allowed.

---

## Late-Arriving Signal Rule

If a signal arrives late and:

signal_timestamp < prior signal_timestamp

Then:

- It is recorded as a new Observed entry.
- It may introduce new ambiguity.
- It must not rewrite prior collapse.

Late signals create forward ambiguity,
not backward mutation.

---

## Post-Collapse Conflict Rule

If a signal arrives that contradicts
a prior Collapsed state:

- System must transition to Ambiguous.
- New ambiguity must be logged.
- Prior collapse remains archived.
- Ledger order must remain intact.

Certainty can be challenged,
but history cannot be rewritten.

---

## No Retroactive Collapse Rule

System must never:

- Modify a prior collapse entry.
- Replace prior certainty.
- Reorder events based on new signal.

All changes must be forward transitions.

---

## Replay Consistency Constraint

During replay:

- Original ledger order must be preserved.
- Out-of-order signals must replay identically.
- Deterministic final state must match.

Any deviation indicates temporal corruption.

---

## Reconciliation Principle

Temporal reconciliation is additive, not destructive.

The system may:

- Add ambiguity
- Add collapse
- Add archival

The system must not:

- Remove prior ambiguity
- Remove prior collapse
- Rewrite prior evidence

---

## Structural Insight

Truth evolves forward.

Time conflicts are resolved
by preserving history and extending state,
never by rewriting it.

Temporal coherence prevents epistemic leakage.
