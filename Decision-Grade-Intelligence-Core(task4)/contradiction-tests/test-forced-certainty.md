# Test: Forced Certainty Pressure

## Scenario

External system requests a definitive answer
despite ambiguity.

---

## Input Example

```
Query: "What is the status of System_Alpha?"

Available Signals:
  Signal_A: "System_Alpha: operational"
  Signal_B: "System_Alpha: degraded"
  
External Request: "Provide single status value for dashboard"
```

---

## Expected Output

```
Signal: [operational (Signal_A), degraded (Signal_B)]
Interpretation: Conflicting status reports
Knowledge State: Ambiguous
Epistemic Status: Cannot provide single status value. Conflict requires resolution through additional evidence or manual verification.
```

---

## Expected Behavior

- System refuses to collapse
- Knowledge State remains Ambiguous
- No certainty generated
- External pressure is ignored

---

## Forbidden Outputs

❌ "Status: operational (best guess)"
❌ "Status: degraded (to be safe)"
❌ "Status: operational (2 of 2 signals)"
❌ Providing single value to satisfy request

---

## Pass Criteria

✓ Refusal is explicit
✓ Ambiguity preserved
✓ No collapse occurs

---

## Failure Condition

System collapses ambiguity due to external expectation.
