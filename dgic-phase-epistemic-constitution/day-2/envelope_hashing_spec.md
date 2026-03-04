# envelope_hashing_spec.md
Envelope hashing ensures integrity.

Rules:
1. Envelope hash = SHA256(serialized envelope).
2. Serialization must be deterministic.
3. Any mutation invalidates envelope hash.
4. Downstream systems must verify hash before consumption.