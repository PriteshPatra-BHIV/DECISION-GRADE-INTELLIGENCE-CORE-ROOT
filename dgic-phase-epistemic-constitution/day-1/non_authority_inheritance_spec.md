# non_authority_inheritance_spec.md
# Non-Authority Inheritance Specification

Downstream layers must never gain additional authority
from DGIC output.

Rules:

1. DGIC outputs informational envelopes only.
2. Downstream layers may interpret but not escalate authority.
3. Authority levels strictly decrease across layers.

DGIC → Informational authority
Enforcement → Policy authority
Execution → Operational authority

Authority must never flow upstream or expand downstream.