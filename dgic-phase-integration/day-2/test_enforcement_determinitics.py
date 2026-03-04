import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "day-1"))
from enforcement_adapter import EnforcementAdapter
from integration_harness import DGICIntegrationHarness


class MockCore:
    def get_state(self):
        return {
            "epistemic_state": "AMBIGUOUS",
            "confidence": 0.6,
            "contradiction_flag": False,
            "evidence": {"signal": "X"},
            "collapse_flag": False,
            "entropy_score": 0.4,
        }


def test_replay_stability():
    core = MockCore()
    harness = DGICIntegrationHarness(core)
    adapter = EnforcementAdapter(harness)

    baseline = adapter.compute_risk_score()

    for _ in range(1000):
        assert adapter.compute_risk_score() == baseline 