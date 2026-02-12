# Signal Taxonomy

## Purpose

This document defines the classification of signals and their relationship to knowledge states.

Every signal must be categorized before interpretation.

---

## Signal Categories

### 1. Direct Signal
- Observed without intermediary processing
- Traceable to source
- Minimal transformation applied

Maps to: **Known** (if verified)

---

### 2. Derived Signal
- Computed from direct signals
- Transformation is explicit and auditable
- Provenance chain exists

Maps to: **Inferred**

---

### 3. Conflicting Signal
- Multiple signals contradict
- No resolution mechanism available
- All variants must be preserved

Maps to: **Ambiguous**

---

### 4. Absent Signal
- Expected signal is missing
- No data available for required context
- Gap cannot be filled by inference

Maps to: **Unknown**

---

## Signal Quality Levels

### Verified
- Source is authenticated
- Integrity is confirmed
- Timestamp is reliable

### Unverified
- Source is known but not authenticated
- Integrity is assumed
- Provenance is incomplete

### Degraded
- Signal has been transformed multiple times
- Original source is unclear
- Reliability is questionable

---

## Mapping Rules

| Signal Type | Quality | Knowledge State |
|-------------|---------|-----------------|
| Direct | Verified | Known |
| Direct | Unverified | Inferred |
| Direct | Degraded | Ambiguous |
| Derived | Any | Inferred |
| Conflicting | Any | Ambiguous |
| Absent | Any | Unknown |

---

## Prohibition

The system must never:
- Upgrade signal quality without evidence
- Merge conflicting signals into consensus
- Invent signals to fill gaps
- Downgrade Unknown to Ambiguous

---

## Closure

Signal classification is mandatory before any interpretation occurs.
