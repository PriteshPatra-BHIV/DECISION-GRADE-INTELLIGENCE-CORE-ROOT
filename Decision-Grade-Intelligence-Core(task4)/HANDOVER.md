# HANDOVER — Sovereign Intelligence Core (Epistemic Closure)

## Overview

This repository contains the sealed epistemic layer of the
Decision-Grade Intelligence Core.

This layer defines what the system is allowed to assert,
how it handles uncertainty, and when it must refuse to answer.

It does not execute decisions.
It does not enforce actions.
It does not act as authority.

---

## What This Layer Does

- Produces structured intelligence
- Separates signal from interpretation
- Declares explicit knowledge states
- Preserves ambiguity
- Enforces refusal when necessary

---

## What This Layer Does NOT Do

- Execute policies
- Recommend actions as authority
- Collapse uncertainty without evidence
- Hide ambiguity behind confidence
- Predict outcomes

---

## Architectural Position

This layer is designed to sit:

Above raw signals  
Below decision engines  

It informs but never decides.

---

## Integration Guidance

### For Downstream Systems

When consuming intelligence outputs:

1. **Respect Knowledge States**
   - KNOWN: Safe to use as factual input
   - INFERRED: Treat as hypothesis requiring validation
   - AMBIGUOUS: Do not force resolution; escalate to human judgment
   - UNKNOWN: Do not proceed without additional information

2. **Never Collapse Upstream Ambiguity**
   - If intelligence layer reports ambiguity, downstream systems must preserve it
   - Decision engines may choose between options but cannot claim certainty

3. **Honor Refusals**
   - Refusal is not a system error
   - Do not retry with modified parameters to force an answer
   - Escalate to manual review or wait for new evidence

---

## Use Case Examples

### Proper Usage

✓ **Scenario:** Decision engine receives AMBIGUOUS state with two possible interpretations
✓ **Action:** Present both options to human operator with context
✓ **Result:** Decision made with full awareness of uncertainty

✓ **Scenario:** Intelligence layer returns UNKNOWN for missing sensor data
✓ **Action:** Decision engine pauses and requests sensor verification
✓ **Result:** System waits for evidence rather than guessing

### Improper Usage

✗ **Scenario:** Decision engine receives AMBIGUOUS state
✗ **Action:** Applies confidence scoring to select "most likely" option
✗ **Result:** False certainty propagates downstream (VIOLATION)

✗ **Scenario:** Intelligence layer refuses to answer
✗ **Action:** System retries with relaxed parameters or default assumptions
✗ **Result:** Epistemic boundaries violated (VIOLATION)

---

## Migration Path

If replacing an existing intelligence system:

1. **Audit Current System**
   - Identify where certainty is currently assumed
   - Map existing outputs to new knowledge states
   - Document cases where current system over-asserts

2. **Parallel Operation**
   - Run both systems simultaneously
   - Compare outputs for epistemic violations
   - Train operators on new refusal semantics

3. **Gradual Cutover**
   - Start with non-critical decision paths
   - Monitor for downstream systems expecting false certainty
   - Update dependent systems to handle ambiguity

4. **Full Deployment**
   - Retire legacy system only after all consumers updated
   - Maintain audit logs for epistemic compliance

---

## Modification Warning

Any future modification must preserve:

- Explicit uncertainty visibility
- Collapse discipline
- Non-knowledge integrity
- Authority neutrality

Violations invalidate system guarantees.

---

## Sovereign Closure Statement

This intelligence core is sealed at the epistemic level.

It is safe to sit beneath enforcement and orchestration systems
because it cannot over-assert and cannot become authority.
