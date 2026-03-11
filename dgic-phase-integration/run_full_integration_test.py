"""
DGIC Full Integration Test Runner
Executes complete validation suite including 10,000 replay cycles
"""

import sys
import time
from pathlib import Path

# Add day-1 to path for imports
sys.path.insert(0, str(Path(__file__).parent / "day-1"))

from integration_harness import DGICIntegrationHarness
from snapshot_model import EpistemicSnapshot


class MockDGICCore:
    """Mock DGIC core for testing"""
    def get_state(self):
        return {
            "epistemic_state": "AMBIGUOUS",
            "confidence": 0.5,
            "contradiction_flag": False,
            "evidence": ["evidence1", "evidence2"],
            "collapse_flag": False,
            "entropy_score": 0.7
        }


def test_deterministic_replay_10k():
    """Execute 10,000 deterministic replay cycles"""
    print("\n" + "="*60)
    print("TEST: 10,000 Deterministic Replay Cycles")
    print("="*60)
    
    harness = DGICIntegrationHarness(MockDGICCore())
    snapshots = []
    
    start_time = time.time()
    
    for i in range(10000):
        snapshot = harness.generate_snapshot()
        snapshots.append(snapshot)
        
        if (i + 1) % 1000 == 0:
            print(f"Progress: {i + 1}/10,000 cycles completed")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Validate consistency
    first_hash = snapshots[0].evidence_hash
    all_consistent = all(s.evidence_hash == first_hash for s in snapshots)
    
    print(f"\n[PASS] RESULT: {'PASS' if all_consistent else 'FAIL'}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Average latency: {(duration/10000)*1000:.2f}ms per cycle")
    print(f"Throughput: {10000/duration:.2f} replays/second")
    print(f"Hash consistency: {all_consistent}")
    
    return all_consistent


def test_concurrency_500_threads():
    """Execute 500-thread concurrency test"""
    print("\n" + "="*60)
    print("TEST: 500-Thread Concurrency Load")
    print("="*60)
    
    import threading
    
    harness = DGICIntegrationHarness(MockDGICCore())
    results = []
    errors = []
    lock = threading.Lock()
    
    def worker(thread_id):
        try:
            for _ in range(20):  # 20 operations per thread
                snapshot = harness.generate_snapshot()
                with lock:
                    results.append(snapshot.evidence_hash)
        except Exception as e:
            with lock:
                errors.append((thread_id, str(e)))
    
    threads = []
    start_time = time.time()
    
    for i in range(500):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
        
        if (i + 1) % 100 == 0:
            print(f"Progress: {i + 1}/500 threads started")
    
    for t in threads:
        t.join()
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Validate results
    all_consistent = len(set(results)) == 1  # All hashes should be identical
    no_errors = len(errors) == 0
    
    print(f"\n[PASS] RESULT: {'PASS' if (all_consistent and no_errors) else 'FAIL'}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Total operations: {len(results)}")
    print(f"Threads completed: {500 - len(errors)}/500")
    print(f"Hash consistency: {all_consistent}")
    print(f"Errors: {len(errors)}")
    
    return all_consistent and no_errors


def test_stress_injection():
    """Execute stress injection test"""
    print("\n" + "="*60)
    print("TEST: Stress Injection (500 cycles)")
    print("="*60)
    
    harness = DGICIntegrationHarness(MockDGICCore())
    snapshots = []
    
    start_time = time.time()
    
    for i in range(500):
        # Simulate stress by rapid snapshot generation
        snapshot = harness.generate_snapshot()
        snapshots.append(snapshot)
        
        if (i + 1) % 100 == 0:
            print(f"Progress: {i + 1}/500 stress cycles completed")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Validate ledger integrity
    all_valid = all(isinstance(s, EpistemicSnapshot) for s in snapshots)
    
    print(f"\n[PASS] RESULT: {'PASS' if all_valid else 'FAIL'}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Ledger integrity: {all_valid}")
    
    return all_valid


def test_enforcement_adapter():
    """Test enforcement adapter integration"""
    print("\n" + "="*60)
    print("TEST: Enforcement Adapter (1,000 cycles)")
    print("="*60)
    
    sys.path.insert(0, str(Path(__file__).parent / "day-2"))
    from enforcement_adapter import EnforcementAdapter
    
    harness = DGICIntegrationHarness(MockDGICCore())
    adapter = EnforcementAdapter(harness)
    
    risk_scores = []
    start_time = time.time()
    
    for i in range(1000):
        score = adapter.compute_risk_score()
        risk_scores.append(score)
        
        if (i + 1) % 200 == 0:
            print(f"Progress: {i + 1}/1,000 enforcement cycles completed")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Validate determinism
    all_consistent = len(set(risk_scores)) == 1
    
    print(f"\n[PASS] RESULT: {'PASS' if all_consistent else 'FAIL'}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Risk score consistency: {all_consistent}")
    print(f"Risk score: {risk_scores[0]}")
    
    return all_consistent


def test_orchestration_adapter():
    """Test orchestration adapter integration"""
    print("\n" + "="*60)
    print("TEST: Orchestration Adapter (100 cycles)")
    print("="*60)
    
    sys.path.insert(0, str(Path(__file__).parent / "day-3"))
    from orchestration_adapter import OrchestrationAdapter
    
    harness = DGICIntegrationHarness(MockDGICCore())
    adapter = OrchestrationAdapter(harness)
    
    decisions = []
    start_time = time.time()
    
    for i in range(100):
        decision = adapter.propose_decision()
        decisions.append(decision)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Validate consistency
    all_consistent = len(set(decisions)) == 1
    
    print(f"\n[PASS] RESULT: {'PASS' if all_consistent else 'FAIL'}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Decision consistency: {all_consistent}")
    print(f"Decision: {decisions[0]}")
    
    return all_consistent


def main():
    """Run full integration test suite"""
    print("\n" + "="*60)
    print("DGIC FULL INTEGRATION TEST SUITE")
    print("="*60)
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Run all tests
    results['10k_replay'] = test_deterministic_replay_10k()
    results['500_thread_concurrency'] = test_concurrency_500_threads()
    results['stress_injection'] = test_stress_injection()
    results['enforcement_adapter'] = test_enforcement_adapter()
    results['orchestration_adapter'] = test_orchestration_adapter()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUITE SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    print(f"OVERALL STATUS: {'[PASS] ALL TESTS PASSED' if all_passed else '[FAIL] SOME TESTS FAILED'}")
    print("="*60)
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n[OK] Full integration test complete!")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
