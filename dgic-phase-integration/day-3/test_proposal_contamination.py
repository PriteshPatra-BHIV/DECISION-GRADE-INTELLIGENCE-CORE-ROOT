import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "day-1"))
sys.path.insert(0, str(Path(__file__).parent.parent / "day-2"))
sys.path.insert(0, str(Path(__file__).parent))

from integration_harness import DGICIntegrationHarness
from orchestration_adapter import OrchestrationAdapter


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


def test_orchestrator_cannot_mutate():
    """Test that orchestrator cannot mutate DGIC core state"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    adapter = OrchestrationAdapter(harness)
    
    original_state = core.get_state()
    
    # Try to mutate through adapter
    for _ in range(50):
        adapter.propose_decision()
    
    new_state = core.get_state()
    
    # State should remain unchanged
    assert original_state == new_state, "Orchestrator mutated core state!"


def test_multiple_proposals_consistent():
    """Test that multiple proposals from same state are consistent"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    adapter = OrchestrationAdapter(harness)
    
    # Generate multiple proposals
    proposals = []
    for _ in range(10):
        proposal = adapter.propose_decision()
        proposals.append(proposal)
    
    # All proposals should be identical
    assert len(set(proposals)) == 1, "Proposals are not consistent!"
    assert proposals[0] == "REQUEST_MORE_DATA", "Unexpected proposal value!"
