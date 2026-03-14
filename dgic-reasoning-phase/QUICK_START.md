# Quick Start Guide - DGIC Reasoning Layer

## 5-Minute Setup

### 1. Verify Installation

```bash
python deployment.py
```

Expected output: `READY FOR PRODUCTION DEPLOYMENT`

### 2. Run Tests

```bash
python test_production.py
```

Expected: All tests pass ✓

### 3. Validate Determinism

```bash
python determinism_validation.py
```

Expected: `DETERMINISM VALIDATED` ✓

---

## Basic Usage

### Create Epistemic States

```python
from multi_state_model import EpistemicState, EpistemicStateSet

# Create individual states
threat_state = EpistemicState(
    epistemic_state="THREAT",
    confidence=0.6,
    entropy=0.4,
    evidence_set=["S1"]
)

sensor_state = EpistemicState(
    epistemic_state="SENSOR_ERROR",
    confidence=0.3,
    entropy=0.7,
    evidence_set=["S2"]
)

# Add to state set
state_set = EpistemicStateSet()
state_set.add_state(threat_state)
state_set.add_state(sensor_state)
```

### Evolve States with Evidence

```python
from state_evolution_engine import StateEvolutionEngine

engine = StateEvolutionEngine()

# New evidence arrives
evidence = {
    "signal_id": "S3",
    "type": "THREAT"
}

# Evolve states
evolved_set = engine.evolve_states(state_set, evidence)

# Check results
for state in evolved_set.get_states():
    print(f"{state.epistemic_state}: confidence={state.confidence:.2f}")
```

### Apply Hypothesis Interference

```python
from state_interference_model import StateInterferenceModel

model = StateInterferenceModel()

# Apply interference
interfered_set = model.apply_interference(evolved_set)

# Compatible states reinforce, conflicting states weaken
for state in interfered_set.get_states():
    print(f"{state.epistemic_state}: confidence={state.confidence:.2f}")
```

### Evaluate Collapse

```python
from collapse_policy_engine import CollapsePolicyEngine

engine = CollapsePolicyEngine()

# Check if uncertainty should collapse
result = engine.evaluate_collapse(interfered_set)

if result:
    print(f"Collapsed to: {result.epistemic_state}")
else:
    print("Ambiguity preserved - multiple hypotheses remain active")
```

### Propagate Knowledge Across Nodes

```python
from knowledge_propagation_model import KnowledgePropagationModel

model = KnowledgePropagationModel()

# Create node states
node1_states = EpistemicStateSet()
node1_states.add_state(EpistemicState("THREAT", 0.8, 0.2, ["S1"]))

node2_states = EpistemicStateSet()
node2_states.add_state(EpistemicState("THREAT", 0.6, 0.4, ["S2"]))

# Aggregate knowledge
global_state = model.propagate([node1_states, node2_states])

# Result: averaged confidence across nodes
for state in global_state.get_states():
    print(f"Global {state.epistemic_state}: confidence={state.confidence:.2f}")
```

---

## Error Handling

```python
from exceptions import ValidationError, EvolutionError
from logger import get_logger

logger = get_logger()

try:
    # Invalid confidence (> 1.0)
    bad_state = EpistemicState("THREAT", 1.5, 0.3, ["S1"])
except ValidationError as e:
    logger.error(f"Invalid state: {e}")

try:
    # Missing required evidence field
    bad_evidence = {"signal_id": "S2"}  # Missing "type"
    evolved = engine.evolve_states(state_set, bad_evidence)
except ValidationError as e:
    logger.error(f"Invalid evidence: {e}")

try:
    # Evolution operation fails
    evolved = engine.evolve_states(state_set, evidence)
except EvolutionError as e:
    logger.error(f"Evolution failed: {e}")
```

---

## Configuration

### Environment Variables

```bash
export DGIC_LOG_LEVEL=DEBUG
export DGIC_LOG_FILE=/var/log/dgic/reasoning.log
export DGIC_CONFIDENCE_THRESHOLD=0.85
export DGIC_ENTROPY_FLOOR=0.2
```

### JSON Configuration

```json
{
    "confidence_threshold": 0.85,
    "entropy_floor": 0.2,
    "dominance_gap": 0.25,
    "log_level": "INFO",
    "log_file": "/var/log/dgic/reasoning.log"
}
```

```python
from config import ReasoningConfig, set_config

config = ReasoningConfig.from_file("config.json")
set_config(config)
```

---

## Complete Example

```python
from multi_state_model import EpistemicState, EpistemicStateSet
from state_evolution_engine import StateEvolutionEngine
from state_interference_model import StateInterferenceModel
from collapse_policy_engine import CollapsePolicyEngine
from logger import get_logger

logger = get_logger()

# 1. Initialize states
state_set = EpistemicStateSet()
state_set.add_state(EpistemicState("THREAT", 0.6, 0.4, ["S1"]))
state_set.add_state(EpistemicState("SENSOR_ERROR", 0.3, 0.7, ["S2"]))

logger.info("Initial states created")

# 2. Evolve with evidence
evolution_engine = StateEvolutionEngine()
evidence = {"signal_id": "S3", "type": "THREAT"}
state_set = evolution_engine.evolve_states(state_set, evidence)

logger.info("States evolved with evidence")

# 3. Apply interference
interference_model = StateInterferenceModel()
state_set = interference_model.apply_interference(state_set)

logger.info("Interference applied")

# 4. Evaluate collapse
collapse_engine = CollapsePolicyEngine()
result = collapse_engine.evaluate_collapse(state_set)

if result:
    logger.info(f"Collapsed to: {result.epistemic_state}")
else:
    logger.info("Ambiguity preserved")

# 5. Output results
for state in state_set.get_states():
    print(f"{state.epistemic_state}: confidence={state.confidence:.2f}, entropy={state.entropy:.2f}")
```

---

## Logging

```python
from logger import get_logger

logger = get_logger()

# Different log levels
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error")
```

---

## Health Checks

```python
from deployment import HealthCheck

# Full health check
health = HealthCheck.full_health_check()

if health["status"] == "HEALTHY":
    print("✓ System is healthy")
else:
    print("✗ System has issues:")
    for check, passed in health["checks"].items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
```

---

## Common Issues

### Issue: ValidationError on state creation

**Cause**: Invalid confidence or entropy value

**Solution**: Ensure values are in [0, 1]

```python
# ✗ Wrong
state = EpistemicState("THREAT", 1.5, 0.3, ["S1"])

# ✓ Correct
state = EpistemicState("THREAT", 0.7, 0.3, ["S1"])
```

### Issue: EvolutionError

**Cause**: Missing required evidence fields

**Solution**: Ensure evidence has "signal_id" and "type"

```python
# ✗ Wrong
evidence = {"signal_id": "S2"}

# ✓ Correct
evidence = {"signal_id": "S2", "type": "THREAT"}
```

### Issue: No collapse when expected

**Cause**: Collapse conditions not met

**Solution**: Check confidence, entropy, and dominance gap

```python
# Check collapse conditions
state = result_state
config = get_config()

print(f"Confidence: {state.confidence} >= {config.confidence_threshold}?")
print(f"Entropy: {state.entropy} <= {config.entropy_floor}?")
print(f"Dominance gap sufficient?")
```

---

## Next Steps

1. **Read Full Documentation**: See `PRODUCTION_API.md`
2. **Review Test Suite**: See `test_production.py`
3. **Check Configuration**: See `config.py`
4. **Monitor Logs**: Use `logger.get_logger()`
5. **Run Health Checks**: Use `HealthCheck.full_health_check()`

---

## Support

- **API Documentation**: `PRODUCTION_API.md`
- **Configuration Guide**: `config.py`
- **Error Handling**: `exceptions.py`
- **Testing**: `test_production.py`
- **Deployment**: `deployment.py`

---

## Status

✅ **PRODUCTION READY**

All systems validated and ready for deployment.
