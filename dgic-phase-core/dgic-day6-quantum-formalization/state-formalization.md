# State Formalization — Classical Density Model

## Purpose

This document formalizes epistemic states using
a density-style classical uncertainty representation.

The system does not collapse uncertainty silently.
It represents uncertainty explicitly.

---

## Classical Density Representation

Instead of a single label, each entity is represented as:

P(Known)
P(Inferred)
P(Ambiguous)
P(Unknown)

Where:

Sum(P) = 1

This mirrors quantum density operators
but in classical probability form.

---

## Interpretation

- Known → certainty weight = 1.0
- Ambiguous → distributed probability
- Unknown → epistemic ignorance
- Inferred → weighted but not absolute

---

## Collapse Rule

Collapse requires:

- P(Known) → 1.0
- All others → 0.0
- Evidence-bound justification
- Ledger logging

No implicit normalization allowed.

---

## Integrity Rule

Uncertainty must be:

- Explicit
- Preserved
- Measurable
- Non-fabricated

False certainty is disallowed.