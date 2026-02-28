# False Certainty Detection

## Purpose

Detect attempts to reduce uncertainty without evidence.

---

## Detection Conditions

Violation if:

- P(Known) increases
- Entropy decreases
- No collapse event logged
- No evidence provided

---

## Prevention Mechanism

System enforces:

- Evidence-bound collapse only
- Hash-chained logging
- Deterministic replay

---

## Guarantee

Certainty cannot appear spontaneously.