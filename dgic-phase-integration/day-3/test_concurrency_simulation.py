import sys
import threading
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


def test_concurrency_safety():
    """Test that concurrent proposals are safe"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    adapter = OrchestrationAdapter(harness)
    
    results = []
    errors = []
    lock = threading.Lock()
    
    def worker():
        try:
            for _ in range(5):
                proposal = adapter.propose_decision()
                with lock:
                    results.append(proposal)
        except Exception as e:
            with lock:
                errors.append(str(e))
    
    # Create 50 threads
    threads = []
    for _ in range(50):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    
    # Wait for all threads
    for t in threads:
        t.join()
    
    # Verify no errors
    assert len(errors) == 0, f"Concurrency errors: {errors}"
    
    # Verify all results are consistent
    assert len(results) == 250, f"Expected 250 results, got {len(results)}"
    assert all(r == "REQUEST_MORE_DATA" for r in results), "Inconsistent proposals!"


def test_parallel_snapshot_access():
    """Test that parallel snapshot access is safe"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    
    snapshots = []
    errors = []
    lock = threading.Lock()
    
    def worker():
        try:
            for _ in range(10):
                snapshot = harness.generate_snapshot()
                with lock:
                    snapshots.append(snapshot.evidence_hash)
        except Exception as e:
            with lock:
                errors.append(str(e))
    
    # Create 50 threads
    threads = []
    for _ in range(50):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    
    # Wait for all threads
    for t in threads:
        t.join()
    
    # Verify no errors
    assert len(errors) == 0, f"Concurrency errors: {errors}"
    
    # Verify all snapshots have same hash (deterministic)
    assert len(set(snapshots)) == 1, "Snapshot hashes are not consistent!"
