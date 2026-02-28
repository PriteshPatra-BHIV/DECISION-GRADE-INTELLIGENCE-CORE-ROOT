# Decision-Grade Intelligence Core

A non-authoritative intelligence system designed to produce structured truth with explicit uncertainty, while refusing decision authority.

## Purpose

This system sits **beneath enforcement, orchestration, and decision layers** to provide:
- Structured intelligence with explicit uncertainty
- Multiple interpretations of signals
- Policy suggestions without execution authority
- Bounded learning without control

## Core Principles

- Intelligence ≠ Decision
- Knowledge ≠ Authority  
- Learning ≠ Control
- Uncertainty is preserved, never collapsed

## What This System Does

- Interprets signals into structured intelligence
- Generates multiple hypotheses with confidence estimates
- Preserves and reports uncertainty explicitly
- Suggests policies hypothetically (never executes)
- Learns under strict supervision (never autonomously)

## What This System Never Does

- Makes decisions
- Executes actions
- Ranks policies for execution
- Optimizes for rewards
- Claims authority or correctness

## Architecture

```
core/
  intelligence_core.py      - Main intelligence processing
  uncertainty_model.py      - Uncertainty tracking and decay
  refusal_layer.py          - Authority boundary enforcement
  output_formatter.py       - Contract-compliant output generation

learning/
  policy_suggestion_engine.py  - Non-authoritative policy suggestions
  bounded_learning_rules.py    - Supervised learning constraints
  supervision_gate.py          - Learning approval mechanism

contracts/
  output-contracts-v2.md       - Output format specification
  non-authority-guarantees.md  - Authority exclusion guarantees
  schema.json                  - JSON schema for outputs

docs/
  HANDOVER.md                  - Ownership transfer guide
  intelligence-vs-decision.md  - Boundary definitions
  system-guarantees.md         - System guarantees
  learning-without-authority.md - Learning constraints
  misuse-prevention.md         - Misuse scenarios and prevention
```

## Usage

### Basic Usage (Direct)
```python
from core.intelligence_core import IntelligenceCore

core = IntelligenceCore()
output = core.process_signals([
    {"signal_id": "S1", "value": 0.8, "source": "sensor"}
])

# Output contains intelligence, uncertainty, and explicit non-guarantees
# Output never contains decisions or action commands
```

### Public API Usage (Recommended)
```python
from api import create_api

api = create_api()

# Process signals
output = api.process_signals([
    {"signal_id": "S1", "value": 0.8, "source": "sensor"}
])

# Get policy suggestions
suggestions = api.suggest_policies(
    context={"state": "operational"},
    observations=[{"signal_id": "S1"}]
)

# Check system status
status = api.get_system_status()
```

## Safety Guarantees

- Authority structurally excluded
- Uncertainty always explicit
- Learning requires supervision
- Fails closed on ambiguity
- Auditable via static inspection

## Integration

When integrating:
- Treat outputs as read-only intelligence
- Never map outputs directly to actions
- Preserve uncertainty downstream
- Require explicit external decision layers

## Documentation

See `docs/HANDOVER.md` for complete ownership transfer guide.

## Status

System complete and ready for integration beneath enforcement layers.
