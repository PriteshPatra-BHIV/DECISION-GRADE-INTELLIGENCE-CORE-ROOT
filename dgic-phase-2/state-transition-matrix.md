# State Transition Matrix

## Purpose

This document formally defines all allowed and forbidden
transitions between epistemic knowledge states.

The system must never promote certainty without justification.

---

## Knowledge States

- Known
- Inferred
- Ambiguous
- Unknown

---

## Allowed Transitions

1. Known → Inferred  
   (Reinterpretation allowed, but not demotion of provenance.)

2. Inferred → Ambiguous  
   (When conflicting interpretations appear.)

3. Ambiguous → Unknown  
   (If signals are removed or invalidated.)

4. Unknown → Ambiguous  
   (If partial signals are introduced.)

5. Inferred → Known  
   (Only with new evidence.)

6. Ambiguous → Known  
   (Only with new evidence AND justified collapse.)

---

## Forbidden Transitions

- Unknown → Known (without new evidence)
- Unknown → Inferred (without signal)
- Ambiguous → Known (without collapse justification)
- Inferred → Known (without new evidence)
- Known → Unknown (state erasure forbidden)
- Any silent promotion of certainty

---

## State Integrity Rule

Transitions must always move toward
greater epistemic honesty,
never toward artificial certainty.

---

## Enforcement Requirements

Every transition must be:

- Explicit
- Logged
- Justified
- Auditable

Unlogged transitions are invalid.
