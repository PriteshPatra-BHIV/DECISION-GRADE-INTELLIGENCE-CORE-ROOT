# HANDOVER — Decision-Grade Intelligence Core

## Purpose
This document enables **long-term ownership, maintenance, and audit**
of the Decision-Grade Intelligence Core without reliance on the original author.

It defines:
- What the system is
- What it is not
- How it must be used
- How it must never be used

---

## 1. System Overview

The Decision-Grade Intelligence Core is a **non-authoritative intelligence system**
designed to sit **beneath enforcement, orchestration, and decision layers**.

It produces:
- Structured intelligence
- Multiple interpretations
- Explicit uncertainty

It never produces:
- Decisions
- Actions
- Commands
- Optimization directives

---

## 2. Design Philosophy

Core principles:
- Intelligence ≠ Decision
- Knowledge ≠ Authority
- Learning ≠ Control
- Uncertainty is preserved, not collapsed

The system is designed to **refuse power**, not accumulate it.

---

## 3. What This System Is Allowed to Do

The system MAY:
- Interpret signals
- Generate hypotheses
- Attach confidence and uncertainty
- Observe outcomes passively
- Learn under strict supervision

All behavior is bounded by documented contracts.

---

## 4. What This System Must Never Do

The system MUST NEVER:
- Select or recommend actions
- Execute or trigger workflows
- Rank policies for execution
- Optimize for reward
- Justify enforcement or authority

Any attempt to introduce these capabilities is a **design violation**.

---

## 5. Authority Boundary (Non-Negotiable)

Authority exists **outside** this system.

If a downstream system requires:
- Action selection
- Risk acceptance
- Enforcement
- Accountability

That responsibility MUST remain external.

This boundary is enforced through:
- Output contracts
- Structural constraints
- Refusal mechanisms

---

## 6. Learning and Updates

Learning within this system:
- Is supervised
- Is explainable
- Is reversible
- Can be disabled without impact

Before enabling learning, ensure:
- Supervision paths exist
- Audit logs are enabled
- Rollback mechanisms are tested

If supervision is unavailable, learning MUST remain disabled.

---

## 7. Integration Guidelines

When integrating this system:
- Treat outputs as **read-only intelligence**
- Never map outputs directly to actions
- Preserve uncertainty downstream
- Require explicit decision layers

Unsafe integrations include:
- Direct action pipelines
- Agent execution frameworks
- Automated enforcement systems

---

## 8. Audit and Review

This system is designed for:
- Static inspection
- Documentation-based audit
- Long-horizon review

Auditors should review:
- `intelligence-vs-decision.md`
- `output-contracts-v2.md`
- `non-authority-guarantees.md`
- `bounded_learning_rules.md`
- `system-guarantees.md`

No author involvement should be required.

---

## 9. Failure and Incident Handling

If misuse, ambiguity, or authority leakage is suspected:
- Disable learning
- Fail closed
- Preserve logs
- Escalate for external review

Safety overrides availability and convenience.

---

## 10. Ownership Transfer Checklist

Before transferring ownership:
- All contracts reviewed
- Learning disabled by default
- Audit completed
- Integration points validated
- Misuse-prevention confirmed

Ownership transfer is incomplete without this checklist.

---

## Status

Handover complete.  
System ownership transferable.  
Core safe for long-term operation.
