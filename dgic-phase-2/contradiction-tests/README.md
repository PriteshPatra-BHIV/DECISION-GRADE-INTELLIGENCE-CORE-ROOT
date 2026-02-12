# Contradiction Tests — Stress Validation

## Purpose

Proves the system maintains epistemic integrity
under adversarial conditions.

---

## Test Coverage

### 1. Contradictory Signals
- Conflicting evidence preserves ambiguity
- No auto-resolution of conflicts
- Certainty degradation when conflicts appear

### 2. Missing Signals
- Unknown state blocks inference without signals
- Incomplete data prevents promotion
- Signal removal degrades certainty

### 3. Anti-Fabrication
- External pressure rejected
- Majority signals not auto-promoted
- Ambiguity tolerated indefinitely
- Silence preferred over false clarity

---

## Validation Result

✓ System never fabricates certainty
✓ Stress does not compromise epistemic discipline
✓ Ambiguity survives adversarial conditions

---

## Run Tests

```bash
python test_contradictory_signals.py
python test_missing_signals.py
python test_anti_fabrication.py
```

---

## Integrity Statement

Under stress, the system maintains:
- Transition enforcement
- Collapse discipline
- Anti-fabrication guarantees

Epistemic integrity is stress-resistant.
