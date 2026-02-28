# Integration Consumption Guide

## Purpose

Define how downstream systems consume epistemic outputs.

---

## Output Structure

Each output contains:

- epistemic_state
- temporal_state
- entropy_value
- evidence_reference (if collapsed)
- hash_reference

---

## What Downstream Systems May Do

- Read epistemic state
- Use entropy for decision support
- Evaluate uncertainty

---

## What Downstream Systems Must NOT Do

- Modify epistemic state
- Trigger collapse
- Rewrite ledger
- Alter timestamps

---

## Contract

Intelligence Core informs.
It does not decide.
It does not enforce.
It does not act.

Authority remains external.