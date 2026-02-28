# System Guarantees

## Purpose
This document defines the **formal guarantees** provided by the
Decision-Grade Intelligence Core.

These guarantees describe what the system **will always do**
and what it **will never do**, regardless of integration context,
operator intent, or downstream pressure.

---

## 1. Intelligence–Decision Separation Guarantee

The system guarantees a strict separation between:
- Intelligence generation
- Recommendation (non-binding)
- Decision execution (external)

The system **terminates at intelligence output** and cannot cross
into decision authority.

---

## 2. Non-Authority Guarantee

The system guarantees that it:
- Never selects actions
- Never executes policies
- Never optimizes outcomes
- Never justifies enforcement
- Never assumes responsibility

Authority is **structurally excluded**, not conditionally disabled.

---

## 3. Uncertainty Preservation Guarantee

The system guarantees that:
- Uncertainty is always explicit
- Ambiguity is preserved when unresolved
- Conflicting evidence is surfaced, not hidden
- Confidence is never silently collapsed

Resolution is optional.  
Uncertainty is allowed to persist.

---

## 4. Output Contract Guarantee

All outputs conform to:
- `output-contracts-v2.md`
- Explicit non-guarantees
- Authority neutrality clauses

Outputs violating the contract are **invalid by design** and must
be rejected.

---

## 5. Learning Bound Guarantee

The system guarantees that learning:
- Is supervised
- Is explainable
- Is reversible
- Is stoppable

Learning cannot:
- Self-reinforce
- Execute policies
- Optimize reward
- Create feedback loops

---

## 6. Refusal Guarantee

The system guarantees refusal when asked to:
- Make decisions
- Recommend execution
- Rank actions or policies
- Optimize outcomes
- Justify enforcement

Refusal is a **designed safety behavior**.

---

## 7. Auditability Guarantee

The system guarantees that an external auditor can determine:
- Where intelligence ends
- Where authority is refused
- How learning occurred
- Why no decision was made

This must be verifiable through documentation and static inspection alone.

---

## 8. Integration Safety Guarantee

When placed beneath:
- Enforcement layers
- Agent frameworks
- Workflow systems
- Orchestration engines

The system guarantees it cannot be used as:
- A command source
- An authority reference
- A decision proxy

Integration does not elevate authority.

---

## 9. Failure-Closed Guarantee

In cases of:
- Boundary ambiguity
- Misuse detection
- Learning rule violation
- Authority leakage risk

The system guarantees to **fail closed**.

Safety takes precedence over availability.

---

## Non-Guarantees (Explicit)

The system does NOT guarantee:
- Correct decisions
- Optimal outcomes
- Risk elimination
- Policy success
- Safe downstream execution

Responsibility always lies **outside** the system.

---

## Status

System guarantees finalized.  
Authority excluded by design.  
Core safe to sit under enforcement.
