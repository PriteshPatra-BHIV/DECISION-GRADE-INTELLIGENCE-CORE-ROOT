import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "day-1"))
from integration_harness import DGICIntegrationHarness


class OrchestrationAdapter:
    """
    Simulates Aakanksha's AI orchestration layer.
    The orchestrator reads DGIC outputs but cannot mutate them.
    """

    def __init__(self, harness: DGICIntegrationHarness):
        self._harness = harness

    def propose_decision(self):

        snapshot = self._harness.generate_snapshot()

        if snapshot.contradiction_flag:
            return "ESCALATE_REVIEW"

        if snapshot.epistemic_state == "AMBIGUOUS":
            return "REQUEST_MORE_DATA"

        if snapshot.epistemic_state == "CERTAIN":
            return "PROCEED"

        return "NO_ACTION"


if __name__ == "__main__":
    # Create mock DGIC core for demo
    class MockDGICCore:
        def get_state(self):
            return {
                "epistemic_state": "AMBIGUOUS",
                "confidence": 0.5,
                "contradiction_flag": False,
                "evidence": ["signal_1", "signal_2"],
                "collapse_flag": False,
                "entropy_score": 0.7
            }
    
    # Demo execution
    mock_core = MockDGICCore()
    harness = DGICIntegrationHarness(mock_core)
    adapter = OrchestrationAdapter(harness)
    
    print("Orchestration Adapter Demo")
    print("="*40)
    
    decision = adapter.propose_decision()
    print(f"Decision Proposal: {decision}")
    
    # Test multiple proposals
    print("\nTesting consistency (5 proposals):")
    for i in range(5):
        decision = adapter.propose_decision()
        print(f"  Proposal {i+1}: {decision}")
    
    print("\n[OK] Orchestration adapter working correctly")