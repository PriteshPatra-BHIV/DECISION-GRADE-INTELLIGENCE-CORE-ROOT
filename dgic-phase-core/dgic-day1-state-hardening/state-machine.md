# Epistemic State Machine — Day 1 Hardening

## Purpose

This document defines the deterministic epistemic state machine
for the Decision-Grade Intelligence Core.

State transitions must be:

- Explicit
- Enforced
- Logged
- Replay-verifiable

---

## Epistemic States

The system operates in exactly four states:

- Known
- Inferred
- Ambiguous
- Unknown

No additional states are permitted.

---

## Allowed Transitions

Unknown → Ambiguous  
Ambiguous → Inferred  
Inferred → Known  
Known → Ambiguous  

Ambiguous → Known (only with new evidence + justified collapse)

---

## Forbidden Transitions

Unknown → Known  
Unknown → Inferred  
Inferred → Unknown  
Known → Unknown  

Any transition not explicitly listed is forbidden.

---

## Determinism Requirement

Given:

- Current state
- Target state
- Evidence flags

The result must always be identical.

No randomness allowed.
