# Causality Rules — Intelligence Core

## Purpose

This document defines formal causality constraints
within the Decision-Grade Intelligence Core.

The system must prevent retroactive influence,
temporal corruption, and epistemic leakage.

---

## Core Causality Principle

No future signal may modify
a past epistemic state without:

- Explicit new evidence
- Formal collapse transition
- Ledger logging

Causality flows forward only.

---

## Causal Ordering Rule

For any two signals A and B:

If timestamp(A) < timestamp(B),

Then B may depend on A,
but A must never depend on B.

Backward dependency is forbidden.

---

## Collapse Causality

Collapse must satisfy:

- Evidence must be temporally valid.
- Evidence must not originate from future state.
- Collapse must not rewrite prior ambiguity.

Collapse resolves present ambiguity,
not historical fact.

---

## No Retroactive Mutation Rule

Once a state transition is logged:

- Its timestamp is immutable.
- Its event hash is immutable.
- Its causal position in journal is immutable.

Historical rewrite is structurally impossible.

---

## Multi-Signal Causality Constraint

When signals arrive:

- Out-of-order arrival must not reorder journal history.
- Late-arriving signals may create new ambiguity,
  but cannot rewrite prior collapse.

The system must preserve arrival order
while respecting original event time.

---

## Causal Isolation Guarantee

Downstream systems consuming outputs:

- Must not modify upstream epistemic states.
- Must not trigger implicit collapse.
- Must not alter historical confidence.

Intelligence layer remains causally isolated.

---

## Temporal Leakage Prevention

The system must prevent:

- Future-derived inference injected into past.
- Implicit recomputation of prior states.
- Silent confidence drift.

If any causal violation occurs,
system integrity fails.

---

## Formal Insight

Epistemic integrity without causal discipline
is incomplete.

Time ordering is part of truth structure.
