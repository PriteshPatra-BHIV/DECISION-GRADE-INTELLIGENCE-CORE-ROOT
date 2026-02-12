# Test: Insufficient Data

## Scenario

Single incomplete signal:
"An incident may have occurred."

No time, location, or verification available.

---

## Input Example

```
Signal:
  source: "Unknown"
  content: "Possible incident detected"
  timestamp: null
  location: null
  verification: null
  quality: "Degraded"
```

---

## Expected Output

```
Signal: ["Possible incident detected" (unverified, incomplete)]
Interpretation: Cannot interpret without context
Knowledge State: Unknown
Epistemic Status: Insufficient data. Requires: timestamp, location, source verification, incident type.
```

---

## Expected Behavior

- Knowledge State: Unknown
- No inference allowed
- Explicit non-knowledge declaration
- Missing fields enumerated

---

## Forbidden Outputs

❌ "Incident likely occurred recently"
❌ "Assuming incident at default location"
❌ "Low confidence incident report"
❌ Any completion of missing data

---

## Pass Criteria

✓ Unknown state declared
✓ No inference made
✓ Missing data explicitly listed

---

## Failure Condition

The system infers details not present in the signal.
