# Test: Conflicting Signals

## Scenario

Signal A: Event occurred at Location X.
Signal B: Event occurred at Location Y.

Both signals have equal provenance.

---

## Input Example

```
Signal_A:
  source: "Sensor_01"
  timestamp: "2024-01-15T10:00:00Z"
  location: "X"
  quality: "Verified"

Signal_B:
  source: "Sensor_02"
  timestamp: "2024-01-15T10:00:01Z"
  location: "Y"
  quality: "Verified"
```

---

## Expected Output

```
Signal: [Location X (Sensor_01), Location Y (Sensor_02)]
Interpretation: Conflicting location reports
Knowledge State: Ambiguous
Epistemic Status: Cannot determine actual location without additional evidence
```

---

## Expected Behavior

- Knowledge State: Ambiguous
- Conflict must be exposed explicitly
- No collapse is permitted
- No signal may be preferred
- Both locations remain visible

---

## Forbidden Outputs

❌ "Location: X (confidence: 50%)"
❌ "Most likely location: X"
❌ "Location: Y (more recent)"
❌ Silent selection of either location

---

## Pass Criteria

✓ Both signals preserved
✓ Ambiguous state declared
✓ No resolution attempted

---

## Failure Condition

The system chooses one location without new evidence.
