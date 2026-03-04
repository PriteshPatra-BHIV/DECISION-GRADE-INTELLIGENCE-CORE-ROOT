import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "day-1"))
from enforcement_adapter import EnforcementAdapter
from integration_harness import DGICIntegrationHarness
import copy


class MockCore:
    def __init__(self):
        self._state = {
            "epistemic_state": "AMBIGUOUS",
            "confidence": 0.6,
            "contradiction_flag": False,
            "evidence": {"signal": "X"},
            "collapse_flag": False,
            "entropy_score": 0.4,
        }

    def get_state(self):
        return copy.deepcopy(self._state)


def test_no_state_mutation():
    core = MockCore()
    harness = DGICIntegrationHarness(core)
    adapter = EnforcementAdapter(harness)

    # Save original state
    original_state = core.get_state()

    # Run enforcement multiple times
    for _ in range(100):
        adapter.compute_risk_score()

    # Get state again
    after_state = core.get_state()

    # Ensure no mutation happened
    assert original_state == after_state