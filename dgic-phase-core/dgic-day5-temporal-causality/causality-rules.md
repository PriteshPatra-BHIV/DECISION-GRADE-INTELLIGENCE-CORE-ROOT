# Causality Rules — Intelligence Core

## Purpose

This document formalizes causality inside the
Decision-Grade Intelligence Core.

The system must prevent:

- Future influencing the past
- Retroactive collapse
- Silent historical mutation
- Temporal corruption

---

## Core Causality Principle

If event A happens before event B,

Then B may depend on A,
but A must never depend on B.

Causality flows forward only.

---

## Timestamp Model

Each signal has:

- signal_timestamp (external origin time)
- event_timestamp (system ingestion time)

Ledger ordering is defined by event_timestamp.

Signal timestamps may be earlier,
but cannot rewrite ledger order.

---

## No Retroactive Mutation Rule

Once a collapse is logged:

- Its timestamp cannot change.
- Its hash cannot change.
- Its ledger position cannot change.

History is immutable.

---

## Late Signal Rule

If a signal arrives late:

signal_timestamp < previous signal_timestamp

Then:

- It is appended to ledger.
- It may introduce new ambiguity.
- It must not rewrite prior collapse.

Late information creates forward uncertainty,
not backward mutation.

---

## Collapse Causality Constraint

Collapse must satisfy:

- Evidence must exist at collapse time.
- Evidence must not originate from future ledger entry.
- Collapse must not rewrite prior state.

Collapse resolves present ambiguity only.

---

## Causal Isolation Guarantee

Downstream systems:

- Cannot modify epistemic states.
- Cannot trigger implicit collapse.
- Cannot rewrite temporal ordering.

Intelligence core remains causally isolated.

---

## Structural Insight

Causality discipline ensures:

Truth evolves forward.
History cannot be rewritten.
Certainty cannot appear from the future.