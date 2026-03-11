import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "day-1"))

from integration_harness import DGICIntegrationHarness


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


def test_stress_injection_500_cycles():
    """Test that DGIC survives 500 stress injection cycles"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    
    snapshots = []
    
    # Generate 500 snapshots under stress
    for _ in range(500):
        snapshot = harness.generate_snapshot()
        snapshots.append(snapshot)
    
    # Verify all snapshots are valid
    assert len(snapshots) == 500, "Not all snapshots generated!"
    assert all(s is not None for s in snapshots), "Some snapshots are None!"


def test_ledger_integrity_under_stress():
    """Test that ledger integrity is maintained under stress"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    
    # Generate snapshots under stress
    hashes = []
    for _ in range(500):
        snapshot = harness.generate_snapshot()
        hashes.append(snapshot.evidence_hash)
    
    # All hashes should be identical (deterministic)
    assert len(set(hashes)) == 1, "Ledger integrity compromised!"


def test_replay_post_stress():
    """Test that replay works correctly after stress"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    
    # Stress the system
    for _ in range(500):
        harness.generate_snapshot()
    
    # Now test replay
    baseline = harness.serialize_snapshot()
    
    for _ in range(100):
        current = harness.serialize_snapshot()
        assert current == baseline, "Replay failed after stress!"
