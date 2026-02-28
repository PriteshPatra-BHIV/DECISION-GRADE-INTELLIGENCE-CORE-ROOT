# Uncertainty Propagation

## Purpose
This document defines how uncertainty flows through the Sovereign Intelligence Core.

Uncertainty must never shrink without justification.

---

## Core Rule

Uncertainty in input must be visible in output.

If signal is ambiguous, interpretation cannot be certain.

---

## Propagation Rules

### 1. Inherited Uncertainty
If a signal is ambiguous or incomplete:
- All derived interpretations remain ambiguous.
- No certainty may be introduced.

---

### 2. Conflict Preservation
If two signals conflict:
- The system must expose the contradiction.
- The system must not resolve the conflict.
- Both interpretations must remain visible.

Silent averaging is forbidden.

---

### 3. Insufficient Data
If data is insufficient:
- The output state must be "Unknown".
- No inference is allowed.

---

### 4. Accumulated Ambiguity
Adding more ambiguous signals does not reduce ambiguity.

More noise does not equal more knowledge.

---

## Forbidden Behaviors

The system must never:
- Convert ambiguity into low-confidence certainty
- Mask conflict as probabilistic variation
- Assume missing context
- Prefer one signal without justification

---

## Principle

Uncertainty is structural, not temporary.
If uncertainty exists, it must remain visible.

---

## Closure

Any transformation that reduces uncertainty without new evidence
is a violation.
