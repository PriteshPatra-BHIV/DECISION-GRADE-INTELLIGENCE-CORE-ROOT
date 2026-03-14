# DGIC Reasoning Layer - Production API Documentation

## Overview

The DGIC reasoning layer provides deterministic, replay-stable reasoning across multiple epistemic hypotheses. All operations are immutable, observable, and fully auditable.

---

## Core Modules

### 1. Configuration Management (`config.py`)

Centralized configuration with validation and multiple loading strategies.

#### ReasoningConfig

```python
from config import ReasoningConfig, get_config, set_config

# Load from environment variables
config = ReasoningConfig.from_env()

# Load from JSON file
config = ReasoningConfig.from_file("config.json")

# Use default configuration
config = get_config()

# Set global configuration
set_config(config)
```

**Configuration Parameters:**
- `confidence_threshold` (float): Collapse confidence threshold [0-1], default 0.85
- `entropy_floor` (float): Collapse entropy floor [0-1], default 0.2
- `dominance_gap` (float): Dominance gap for collapse [0-1], default 0.25
- `log_level` (str): Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL), default INFO
- `log_file` (str): Optional log file path

---

### 2. Logging Infrastructure (`logger.py`)

Centralized logging for observability and debugging.

```python
from logger import get_logger

logger = get_logger()
logger.info("Processing evidence signal")
logger.error("State evolution failed")
logger.debug("Detailed debug information")
```

---

### 3. Exception Hierarchy (`exceptions.py`)

Comprehensive exception types for error handling.

```python
from exceptions import (
    ValidationError,
    StateError,
    EvolutionError,
    InterferenceError,
    CollapseError,
    PropagationError
)

try:
    state = EpistemicState("THREAT", 1.5, 0.3, ["S1"])
except ValidationError as e:
    logger.error(f"Invalid state: {e}")
```

---

### 4. Multi-State Model (`multi_state_model.py`)

Represents and manages multiple epistemic hypotheses.

#### EpistemicState

Immutable representation of a single hypothesis.

```python
from multi_state_model import EpistemicState

state = EpistemicState(
    epistemic_state="THREAT",
    confidence=0.7,
    entropy=0.3,
    evidence_set=["S1", "S2"]
)

# Access properties
print(state.epistemic_state)  # "THREAT"
print(state.confidence)        # 0.7
print(state.entropy)           # 0.3
print(state.evidence_set)      # ["S1", "S2"]

# Get deterministic evidence hash
hash_value = state.evidence_hash()

# Convert to dictionary
state_dict = state.to_dict()
```

**Validation Rules:**
- `epistemic_state`: Non-empty string
- `confidence`: Float in [0, 1]
- `entropy`: Float in [0, 1]
- `evidence_set`: List of strings

#### EpistemicStateSet

Container for multiple epistemic hypotheses.

```python
from multi_state_model import EpistemicStateSet

state_set = EpistemicStateSet()

# Add states
state_set.add_state(state1)
state_set.add_state(state2)

# Get states in deterministic order
states = state_set.get_states()

# Get number of states
count = state_set.size()

# Convert to serializable format
data = state_set.to_list()
```

---

### 5. State Evolution Engine (`state_evolution_engine.py`)

Evolves epistemic hypotheses when new evidence arrives.

```python
from state_evolution_engine import StateEvolutionEngine

engine = StateEvolutionEngine()

# Evolve states with new evidence
evidence = {
    "signal_id": "S3",
    "type": "THREAT"
}

evolved_set = engine.evolve_states(state_set, evidence)
```

**Evidence Structure:**
- `signal_id` (str): Unique identifier for the signal
- `type` (str): Evidence type (matches epistemic_state or "CONTRADICTION")

**Evolution Rules:**
- Supporting evidence: confidence +0.1, entropy -0.1
- Contradicting evidence: confidence -0.15, entropy +0.1
- Neutral evidence: entropy +0.05

**Exceptions:**
- `ValidationError`: Invalid inputs
- `EvolutionError`: Evolution operation failed

---

### 6. State Interference Model (`state_interference_model.py`)

Handles deterministic interaction between epistemic hypotheses.

```python
from state_interference_model import StateInterferenceModel

model = StateInterferenceModel()

# Apply interference between states
interfered_set = model.apply_interference(state_set)
```

**Interference Rules:**
- Compatible states (same epistemic_state): confidence +0.03, entropy -0.02
- Conflicting states: weaker state loses confidence -0.04, entropy +0.02

**Exceptions:**
- `ValidationError`: Invalid inputs
- `InterferenceError`: Interference calculation failed

---

### 7. Collapse Policy Engine (`collapse_policy_engine.py`)

Determines when epistemic uncertainty collapses to a single hypothesis.

```python
from collapse_policy_engine import CollapsePolicyEngine

engine = CollapsePolicyEngine()

# Evaluate collapse conditions
result = engine.evaluate_collapse(state_set)

if result:
    print(f"Collapsed to: {result.epistemic_state}")
else:
    print("Ambiguity preserved")
```

**Collapse Triggers:**
1. Confidence threshold: confidence >= 0.85
2. Entropy floor: entropy <= 0.2
3. Dominance gap: top_confidence - second_confidence >= 0.25

**Return Value:**
- `EpistemicState`: Collapsed state if conditions met
- `None`: No collapse, ambiguity preserved

**Exceptions:**
- `ValidationError`: Invalid inputs
- `CollapseError`: Collapse evaluation failed

---

### 8. Knowledge Propagation Model (`knowledge_propagation_model.py`)

Simulates distributed knowledge sharing between reasoning nodes.

```python
from knowledge_propagation_model import KnowledgePropagationModel

model = KnowledgePropagationModel()

# Aggregate knowledge from multiple nodes
node1_states = EpistemicStateSet()
node1_states.add_state(EpistemicState("THREAT", 0.8, 0.2, ["S1"]))

node2_states = EpistemicStateSet()
node2_states.add_state(EpistemicState("THREAT", 0.6, 0.4, ["S2"]))

global_state = model.propagate([node1_states, node2_states])
```

**Propagation Rules:**
- Confidence is averaged across nodes
- Evidence sets are merged deterministically
- Entropy is computed as 1 - average_confidence

**Exceptions:**
- `ValidationError`: Invalid inputs
- `PropagationError`: Propagation failed

---

## Error Handling

All modules use consistent exception handling:

```python
from exceptions import ValidationError, EvolutionError
from logger import get_logger

logger = get_logger()

try:
    evolved = engine.evolve_states(state_set, evidence)
except ValidationError as e:
    logger.error(f"Invalid input: {e}")
    # Handle validation error
except EvolutionError as e:
    logger.error(f"Evolution failed: {e}")
    # Handle evolution error
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Handle unexpected error
```

---

## Testing

### Unit Tests

Run comprehensive test suite:

```bash
python test_production.py
```

**Test Coverage:**
- EpistemicState validation (7 tests)
- EpistemicStateSet operations (3 tests)
- State evolution (4 tests)
- State interference (2 tests)
- Collapse policy (5 tests)
- Knowledge propagation (3 tests)
- Determinism validation (2 tests)

### Determinism Validation

Validate replay stability:

```bash
python determinism_validation.py
```

Runs pipeline 100 times and verifies identical output.

---

## Deployment

### Health Check

```python
from deployment import HealthCheck

health = HealthCheck.full_health_check()
print(health["status"])  # "HEALTHY" or "UNHEALTHY"
```

### Production Readiness Report

```bash
python deployment.py
```

Prints comprehensive production readiness report.

---

## Configuration Example

**config.json:**
```json
{
    "confidence_threshold": 0.85,
    "entropy_floor": 0.2,
    "dominance_gap": 0.25,
    "log_level": "INFO",
    "log_file": "/var/log/dgic/reasoning.log"
}
```

**Environment Variables:**
```bash
export DGIC_CONFIDENCE_THRESHOLD=0.85
export DGIC_ENTROPY_FLOOR=0.2
export DGIC_LOG_LEVEL=INFO
export DGIC_LOG_FILE=/var/log/dgic/reasoning.log
```

---

## Performance Characteristics

- **State Evolution**: O(n) where n = number of states
- **Interference**: O(n²) where n = number of states
- **Collapse Evaluation**: O(n log n) due to sorting
- **Knowledge Propagation**: O(n*m) where n = states, m = nodes

---

## Determinism Guarantees

✓ Immutable state objects  
✓ Deterministic ordering  
✓ Fixed evolution rules  
✓ Deterministic interference  
✓ Rule-based collapse policy  
✓ Fully replay-stable  

---

## Support

For issues or questions:
1. Check logs: `logger.get_logger()`
2. Run health check: `HealthCheck.full_health_check()`
3. Review test suite: `test_production.py`
4. Validate determinism: `determinism_validation.py`
