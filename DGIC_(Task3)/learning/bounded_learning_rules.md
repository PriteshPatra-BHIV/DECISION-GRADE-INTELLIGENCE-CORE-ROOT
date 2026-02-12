# Bounded Learning Rules

## Purpose
This document defines the **hard constraints** under which learning is permitted
inside the Decision-Grade Intelligence Core.

These rules ensure learning remains:
- Bounded
- Explainable
- Stoppable
- Non-authoritative

Violation of any rule constitutes a **system failure**.

---

## 1. Learning Permission Scope

Learning is permitted **only** to:
- Update confidence estimates
- Refine interpretation mappings
- Expand hypothesis sets
- Record observed outcomes

Learning is explicitly **not permitted** to:
- Select actions
- Execute policies
- Optimize rewards
- Influence enforcement
- Trigger workflows

---

## 2. Supervision Requirement

All learning updates MUST:
- Be externally approved
- Be traceable to a human or policy authority
- Be reversible

No autonomous learning updates are allowed.

---

## 3. No Self-Reinforcement Rule

The system MUST NOT:
- Use its own outputs as training signals
- Reinforce interpretations based on acceptance
- Optimize toward historical reward patterns

Learning signals must originate **outside** the system.

---

## 4. No Feedback Loops

The system MUST NOT:
- Observe outcomes of its own suggestions
- Adapt based on downstream decisions
- Close the loop between suggestion and outcome

All outcome observation is **passive and delayed**.

---

## 5. No Policy Drift

Policies suggested by the system:
- Are hypothetical
- Do not persist across runs by default
- Must be re-derived per context

Long-term policy memory without review is forbidden.

---

## 6. Update Constraints

All learning updates MUST:
- Declare what changed
- Declare what did not change
- Preserve previous uncertainty states
- Never reduce uncertainty without evidence

Silent updates are forbidden.

---

## 7. Stoppability Guarantee

Learning can be:
- Paused
- Rolled back
- Disabled entirely

Disabling learning MUST NOT impair:
- Intelligence generation
- Uncertainty reporting
- Contract compliance

---

## 8. Explainability Requirement

Every learning update MUST be explainable via:
- Input signals
- Observed outcomes
- Explicit reasoning steps

Black-box updates are prohibited.

---

## 9. Failure Conditions

The system MUST fail closed if:
- Supervision is unavailable
- Learning boundaries are unclear
- Feedback loops are detected
- Authority leakage is suspected

Failure to learn is preferred over unsafe learning.

---

## Status

Learning bounded.  
Authority blocked.  
System safe under audit.
