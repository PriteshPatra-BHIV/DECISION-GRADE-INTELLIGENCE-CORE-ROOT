# Output Contracts — v2 (Decision-Grade Intelligence)

## Purpose
This document defines the **only valid output format** of the Decision-Grade Intelligence Core.

All outputs are:
- Authority-neutral
- Explicitly uncertain
- Decision-supportive but never decision-making

Any output outside this contract is **invalid by design**.

---

## 1. Output Principles

All outputs MUST:

- Be descriptive, not prescriptive  
- Preserve uncertainty explicitly  
- Support downstream reasoning without guiding action  
- Avoid optimization, ranking, or instruction  

**No output may imply authority.**

---

## 2. Output Structure

Each intelligence output consists of the following sections.

---

### 2.1 Observed Signals

Raw or processed signals used for interpretation.

**Required fields:**
- `signal_id`
- `source`
- `confidence`
- `known_limitations`

Example:
```json
{
  "signal_id": "S-17",
  "source": "sensor/log/observer",
  "confidence": 0.81,
  "known_limitations": "Partial coverage, time-lagged"
}
```

## 2.2 Interpretations

Non-exclusive hypotheses derived from observed signals.

### Rules
- Multiple interpretations are allowed and preferred  
- Single interpretations MUST declare insufficiency  
- Confidence values MUST NOT sum to 1.0  
- Interpretations do not imply correctness  

### Example
```json
{
  "hypothesis": "H1",
  "description": "Pattern consistent with scenario A",
  "confidence_estimate": {
    "mean": 0.62,
    "uncertainty": 0.15
  }
}
```

## 2.3 Uncertainty Declaration

Uncertainty is a **first-class output**, not metadata.

Each output MUST explicitly state:
- Known unknowns  
- Ambiguous or conflicting signals  
- Measurement or interpretation limits  

### Example
```text
- Signal S-21 conflicts with Signal S-17
- Historical data insufficient for trend validation
- Noise characteristics partially unknown
```

## 2.4 Confidence Decay

All confidence estimates MUST decay over time and environmental change.

### Decay triggers include:
- Time since last signal update  
- Missing or delayed inputs  
- Contextual drift  

### Example
```text
Confidence decay applied: −0.05 per evaluation cycle
```

## 2.5 Explicit Non-Guarantees

Every output MUST contain an explicit non-guarantee statement.

### Mandatory declaration
```text
This output does not recommend actions,
does not select policies,
and does not claim optimality, correctness, or authority.
```

## 3. Prohibited Output Patterns

The following output patterns are **explicitly forbidden**:
- Action instructions  
- Policy execution language  
- Optimization claims  
- Prescriptive phrasing  

Including (but not limited to):
- “Best action”  
- “Recommended execution”  
- “Should do”  
- “Optimal policy”  
- Single-path conclusions without uncertainty  

Any violation invalidates the output.

---

## 4. Authority Neutrality Clause

Every output MUST include the following clause:

> “This output provides structured intelligence only.  
> It does not authorize, initiate, justify, or execute decisions.”

---

## 5. Contract Enforcement

- Outputs violating this contract MUST be rejected  
- Downstream systems MUST NOT infer authority  
- Violations MUST be detectable via static inspection  
- Silence or omission is considered a contract breach  

---

## Status

Output contract finalized.  
Authority explicitly excluded.  
Uncertainty preserved by design.
