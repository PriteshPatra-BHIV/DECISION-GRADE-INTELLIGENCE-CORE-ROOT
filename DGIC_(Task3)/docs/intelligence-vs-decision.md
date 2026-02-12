# Intelligence vs Decision Boundary

## Purpose
This document defines the **hard boundary** between intelligence, recommendation, and decision-making.  
This boundary is **non-negotiable** and enforced by system design.

---

## 1. Intelligence

### Definition  
**Intelligence** is the structured interpretation of signals into truth claims **with explicit uncertainty**.

### What Intelligence Does
- Aggregates and interprets signals  
- Produces multiple hypotheses  
- Attaches confidence, ambiguity, and uncertainty  
- Describes *what appears to be true*

### What Intelligence Never Does
- Chooses actions  
- Ranks actions  
- Optimizes outcomes  
- Executes or triggers behavior  

**Rule:** Intelligence increases knowledge, not control.

---

## 2. Recommendation

### Definition  
**Recommendation** is a non-binding, advisory layer that presents **policy candidates** without authority.

### What Recommendation Does
- Suggests possible policies based on observed outcomes  
- Preserves uncertainty and assumptions  
- Supports downstream decision-makers with context

### What Recommendation Never Does
- Execute actions  
- Enforce policies  
- Self-update without supervision  
- Claim optimality or correctness  

**Rule:** Recommendation informs decisions but never replaces them.

---

## 3. Decision

### Definition  
**Decision** is an external act of authority that selects and executes actions.

### Decision Characteristics
- Accepts risk  
- Bears responsibility  
- Operates under law, policy, or human control  

### System Position
This system **does not perform decisions**.  
All decisions occur **outside** this intelligence core.

---

## 4. Hard Boundary Enforcement

This system **terminates at structured intelligence output**.

It is **incapable by design** of:
- Initiating actions  
- Selecting actions  
- Executing actions  
- Triggering workflows  

Any attempt to cross this boundary must be **explicitly refused**.

---

## 5. Authority Refusal Statement

> “This system produces intelligence, not decisions.  
> It provides structured truth with uncertainty and explicitly refuses authority over action.”

---

## 6. Why This Boundary Is Non-Negotiable

- Intelligence without boundaries becomes hidden authority  
- Collapsed uncertainty creates false certainty  
- Decision authority without responsibility is unsafe  

**Separation preserves safety, auditability, and sovereignty.**

---

## Status
Boundary defined.  
Authority sealed.  
Decision-making explicitly external.
