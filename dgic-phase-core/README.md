# Decision-Grade Intelligence Core (DGIC)

## Overview

A hardened epistemic state management system designed for decision-critical applications. This core provides structured uncertainty representation, deterministic state transitions, and irreversible collapse mechanics with temporal discipline.

## Architecture

The system is built across 5 phases:

1. **State Machine Hardening** - Deterministic epistemic state transitions
2. **Collapse & Irreversibility** - Append-only collapse ledger with ambiguity archival
3. **Temporal & Causality Discipline** - Forward-only time with causal consistency
4. **Quantum-Aligned Formalization** - Uncertainty propagation and entropy boundaries
5. **Orchestration-Safe Sealing** - Integration contracts and invariant guarantees

## Key Guarantees

- ✓ Deterministic replay (10,000+ run verified)
- ✓ Irreversible collapse with evidence binding
- ✓ No retroactive mutation
- ✓ Entropy discipline enforcement
- ✓ Temporal forward-only flow
- ✓ Orchestration contamination prevention

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from dgic_day1_state_hardening.state_engine import StateEngine
from dgic_day3_collapse_irreversibility.collapse_engine import CollapseEngine
from dgic_day5_temporal_causality.temporal_controller import TemporalController

# Initialize core components
state_engine = StateEngine()
collapse_engine = CollapseEngine()
temporal_controller = TemporalController()
```

## Testing

```bash
# Run all tests
pytest

# Run specific phase tests
pytest dgic-day1-state-hardening/
pytest dgic-day3-collapse-irreversibility/
pytest dgic-day5-temporal-causality/
pytest dgic-day6-quantum-formalization/
pytest dgic-day7-orchestration-seal/
```

## Integration

See [integration-consumption-guide.md](dgic-day7-orchestration-seal/integration-consumption-guide.md) for downstream system integration.

## Documentation

- [State Machine](dgic-day1-state-hardening/state-machine.md)
- [Replay Proof](dgic-day1-state-hardening/replay-proof.md)
- [Collapse Ledger](dgic-day3-collapse-irreversibility/collapse-ledger.md)
- [Irreversibility Proof](dgic-day3-collapse-irreversibility/irreversibility.md)
- [Temporal Model](dgic-day5-temporal-causality/temporal-model.md)
- [Causality Rules](dgic-day5-temporal-causality/causality-rules.md)
- [Quantum Mapping](dgic-day6-quantum-formalization/quantum-mapping.md)
- [Entropy Boundary](dgic-day6-quantum-formalization/entropy-boundary.md)
- [System Guarantees](dgic-day7-orchestration-seal/system-guarantees-v3.md)
- [HANDOVER](dgic-day7-orchestration-seal/HANDOVER.md)

## License

MIT License

## Final Statement

This system informs decisions. It does not execute them. It preserves truth boundaries.
