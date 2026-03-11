import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "day-1"))
sys.path.insert(0, str(Path(__file__).parent / "day-2"))

from integration_harness import DGICIntegrationHarness
from enforcement_adapter import EnforcementAdapter


class MockDGICCore:
    def get_state(self):
        return {
            "epistemic_state": "AMBIGUOUS",
            "confidence": 0.5,
            "contradiction_flag": False,
            "evidence": ["evidence1", "evidence2"],
            "collapse_flag": False,
            "entropy_score": 0.7
        }


@pytest.fixture
def adapter():
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    return EnforcementAdapter(harness)


@pytest.fixture
def harness():
    """Fixture providing DGICIntegrationHarness for tests"""
    core = MockDGICCore()
    return DGICIntegrationHarness(core)
