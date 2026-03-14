# Epistemic Collapse Policy

## Purpose

The collapse policy determines when epistemic uncertainty transitions from multiple hypotheses to a single dominant hypothesis.

Collapse does not represent absolute truth.  
It represents the most plausible explanation given current evidence.

---

## Collapse Triggers

### 1. Confidence Threshold

If a hypothesis confidence exceeds:

0.85

The system considers the hypothesis strong enough to collapse.

---

### 2. Entropy Floor

If hypothesis entropy falls below:

0.20

The system considers uncertainty sufficiently reduced.

---

### 3. Dominance Gap

If the difference between the top hypothesis and second hypothesis exceeds:

0.25

The dominant hypothesis becomes the collapse candidate.

---

## Non-Collapse Conditions

If none of the triggers activate:

The system preserves ambiguity.

Multiple hypotheses remain active until stronger evidence emerges.

---

## Collapse Guarantees

Collapse decisions remain:

deterministic  
replayable  
evidence-bound  

The system never collapses uncertainty due to randomness or external pressure.

---

## DGIC Safety Principle

Collapse results inform downstream orchestration systems but do not enforce decisions.

Authority remains external to the reasoning engine.