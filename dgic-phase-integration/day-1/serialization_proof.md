# Serialization Discipline Proof

## Determinism Rules

1. JSON keys sorted.
2. No whitespace variance.
3. Evidence hashed using SHA256.
4. Deep copy before snapshot generation.
5. Frozen dataclass ensures immutability.

## Replay Stability

Deterministic replay test included in integration_harness.py

Same input → Same output.

No time dependency.
No randomness.
No hidden state.    