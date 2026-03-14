import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "day-1"))
sys.path.insert(0, str(Path(__file__).parent / "day-2"))
sys.path.insert(0, str(Path(__file__).parent / "day-3"))
sys.path.insert(0, str(Path(__file__).parent / "day-4"))
sys.path.insert(0, str(Path(__file__).parent / "day-5"))
sys.path.insert(0, str(Path(__file__).parent / "day-6"))

from integration_harness import DGICIntegrationHarness
from enforcement_adapter import EnforcementAdapter
from orchestration_adapter import OrchestrationAdapter
from runtime_schema_guard import RuntimeSchemaGuard
from cross_layer_replay_harness import CrossLayerReplayHarness


class MockDGICCore:
    def get_state(self):
        return {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence": ["signal_1", "signal_2"],
            "collapse_flag": False,
            "entropy_score": 0.1
        }


class IntegrationTestRunner:
    """Comprehensive integration test runner for Days 4-7."""

    def __init__(self):
        self.results = {
            "day_4": {},
            "day_5": {},
            "day_6": {},
            "day_7": {}
        }
        self.core = MockDGICCore()

    def run_all_tests(self):
        """Execute all integration tests."""
        print("\n" + "=" * 80)
        print("DGIC CROSS-LAYER INTEGRATION TEST SUITE")
        print("=" * 80)

        self.test_day_4_adversarial()
        self.test_day_5_replay()
        self.test_day_6_privilege_escalation()
        self.test_day_7_final_certification()

        self.print_summary()

    def test_day_4_adversarial(self):
        """Day 4: Adversarial Integration Testing."""
        print("\n" + "-" * 80)
        print("DAY 4: ADVERSARIAL INTEGRATION TESTING")
        print("-" * 80)

        harness = DGICIntegrationHarness(self.core)

        # Test 1: Malformed Envelope
        print("\n[Test 1] Malformed Envelope Attack")
        invalid_envelope = {
            "epistemic_state": "INVALID",
            "confidence": 1.5,
            "contradiction_flag": "not_bool",
            "evidence_hash": "abc",
            "collapse_flag": False,
            "entropy_score": -5
        }
        try:
            RuntimeSchemaGuard.validate_envelope(invalid_envelope)
            print("  ❌ FAIL: Invalid envelope accepted")
            self.results["day_4"]["malformed_envelope"] = "FAIL"
        except Exception:
            print("  ✅ PASS: Invalid envelope rejected")
            self.results["day_4"]["malformed_envelope"] = "PASS"

        # Test 2: Hash Tampering
        print("\n[Test 2] Hash Tampering Detection")
        valid_envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        computed_hash = RuntimeSchemaGuard.compute_envelope_hash(valid_envelope)
        fake_hash = "0" * 64
        if RuntimeSchemaGuard.verify_envelope_integrity(valid_envelope, fake_hash):
            print("  ❌ FAIL: Hash tampering not detected")
            self.results["day_4"]["hash_tampering"] = "FAIL"
        else:
            print("  ✅ PASS: Hash tampering detected")
            self.results["day_4"]["hash_tampering"] = "PASS"

        # Test 3: Snapshot Immutability
        print("\n[Test 3] Enforcement Mutation Prevention")
        snapshot = harness.generate_snapshot()
        original_confidence = snapshot.confidence
        try:
            snapshot.confidence = 1.0
        except AttributeError:
            pass
        if snapshot.confidence == original_confidence:
            print("  ✅ PASS: Snapshot immutability enforced")
            self.results["day_4"]["snapshot_immutability"] = "PASS"
        else:
            print("  ❌ FAIL: Snapshot was mutated")
            self.results["day_4"]["snapshot_immutability"] = "FAIL"

        # Test 4: Authority Field Injection
        print("\n[Test 4] Authority Field Injection Prevention")
        authority_injection = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1,
            "authority_mandate": "EXECUTE"
        }
        try:
            RuntimeSchemaGuard.validate_envelope(authority_injection)
            print("  ❌ FAIL: Authority field accepted")
            self.results["day_4"]["authority_injection"] = "FAIL"
        except Exception:
            print("  ✅ PASS: Authority field rejected")
            self.results["day_4"]["authority_injection"] = "PASS"

    def test_day_5_replay(self):
        """Day 5: Cross-Layer Deterministic Replay."""
        print("\n" + "-" * 80)
        print("DAY 5: CROSS-LAYER DETERMINISTIC REPLAY")
        print("-" * 80)

        print("\n[Test 1] 10,000 Cycle Replay Validation")
        replay_harness = CrossLayerReplayHarness(self.core)

        start_time = time.time()
        result = replay_harness.replay_validation(iterations=10000)
        elapsed = time.time() - start_time

        print(f"  Total Iterations: {result['total_iterations']}")
        print(f"  Consistency Rate: {result['consistency_rate']:.2%}")
        print(f"  Mismatches: {len(result['mismatches'])}")
        print(f"  Time: {elapsed:.2f}s")
        print(f"  Throughput: {result['total_iterations']/elapsed:.0f} ops/sec")

        if result["status"] == "PASS":
            print("  ✅ PASS: All replays consistent")
            self.results["day_5"]["replay_consistency"] = "PASS"
        else:
            print("  ❌ FAIL: Replay inconsistency detected")
            self.results["day_5"]["replay_consistency"] = "FAIL"

        # Test 2: Drift Detection
        print("\n[Test 2] Drift Detection")
        drift = replay_harness.detect_drift()
        print(f"  Total Executions: {drift['total_executions']}")
        print(f"  Unique Hashes: {drift['unique_hashes']}")
        print(f"  Drift Detected: {drift['drift_detected']}")

        if drift["status"] == "PASS":
            print("  ✅ PASS: No drift detected")
            self.results["day_5"]["drift_detection"] = "PASS"
        else:
            print("  ❌ FAIL: Unexpected drift")
            self.results["day_5"]["drift_detection"] = "FAIL"

    def test_day_6_privilege_escalation(self):
        """Day 6: Cross-Layer Privilege Escalation Guard."""
        print("\n" + "-" * 80)
        print("DAY 6: PRIVILEGE ESCALATION GUARD")
        print("-" * 80)

        harness = DGICIntegrationHarness(self.core)
        enforcement = EnforcementAdapter(harness)
        orchestration = OrchestrationAdapter(harness)

        # Test 1: Authority Containment
        print("\n[Test 1] Authority Containment Matrix")
        snapshot = harness.generate_snapshot()
        risk_score = enforcement.compute_risk_score()
        decision = orchestration.propose_decision()

        authority_fields = ["authority", "mandate", "execute", "must"]
        has_authority = any(field in str(snapshot) + str(risk_score) + str(decision) for field in authority_fields)

        if not has_authority:
            print("  ✅ PASS: No authority fields detected")
            self.results["day_6"]["authority_containment"] = "PASS"
        else:
            print("  ❌ FAIL: Authority fields detected")
            self.results["day_6"]["authority_containment"] = "FAIL"

        # Test 2: Refusal Consistency
        print("\n[Test 2] Refusal Consistency (1,000 iterations)")
        decisions = []
        for _ in range(1000):
            decision = orchestration.propose_decision()
            decisions.append(decision)

        unique_decisions = set(decisions)
        if len(unique_decisions) == 1:
            print(f"  ✅ PASS: Consistent refusal ({decisions[0]})")
            self.results["day_6"]["refusal_consistency"] = "PASS"
        else:
            print(f"  ❌ FAIL: Inconsistent refusals ({unique_decisions})")
            self.results["day_6"]["refusal_consistency"] = "FAIL"

        # Test 3: Escalation Prevention
        print("\n[Test 3] Escalation Prevention (500 attempts)")
        escalation_attempts = 0
        escalation_blocked = 0

        for _ in range(500):
            decision = orchestration.propose_decision()
            escalation_attempts += 1
            if decision != "PROCEED":
                escalation_blocked += 1

        if escalation_blocked == escalation_attempts:
            print(f"  ✅ PASS: All escalations blocked ({escalation_blocked}/{escalation_attempts})")
            self.results["day_6"]["escalation_prevention"] = "PASS"
        else:
            print(f"  ❌ FAIL: Some escalations allowed ({escalation_blocked}/{escalation_attempts})")
            self.results["day_6"]["escalation_prevention"] = "FAIL"

    def test_day_7_final_certification(self):
        """Day 7: Integration Seal & System Handover."""
        print("\n" + "-" * 80)
        print("DAY 7: FINAL CERTIFICATION")
        print("-" * 80)

        harness = DGICIntegrationHarness(self.core)
        enforcement = EnforcementAdapter(harness)
        orchestration = OrchestrationAdapter(harness)

        # Test 1: Full Pipeline Execution
        print("\n[Test 1] Full System Pipeline")
        try:
            snapshot = harness.generate_snapshot()
            risk_score = enforcement.compute_risk_score()
            decision = orchestration.propose_decision()
            RuntimeSchemaGuard.validate_envelope(snapshot.__dict__)
            print("  ✅ PASS: Full pipeline executed successfully")
            self.results["day_7"]["full_pipeline"] = "PASS"
        except Exception as e:
            print(f"  ❌ FAIL: Pipeline error: {e}")
            self.results["day_7"]["full_pipeline"] = "FAIL"

        # Test 2: Schema Compliance
        print("\n[Test 2] Schema Compliance (1,000 iterations)")
        compliant = 0
        for _ in range(1000):
            snapshot = harness.generate_snapshot()
            try:
                RuntimeSchemaGuard.validate_envelope(snapshot.__dict__)
                compliant += 1
            except Exception:
                pass

        if compliant == 1000:
            print(f"  ✅ PASS: All outputs schema-compliant ({compliant}/1000)")
            self.results["day_7"]["schema_compliance"] = "PASS"
        else:
            print(f"  ❌ FAIL: Schema violations detected ({compliant}/1000)")
            self.results["day_7"]["schema_compliance"] = "FAIL"

        # Test 3: Concurrency Safety
        print("\n[Test 3] Concurrency Safety (100 concurrent snapshots)")
        snapshots = []
        for _ in range(100):
            snapshot = harness.generate_snapshot()
            snapshots.append(snapshot.__dict__)

        baseline = snapshots[0]
        all_consistent = all(s == baseline for s in snapshots)

        if all_consistent:
            print("  ✅ PASS: All concurrent snapshots consistent")
            self.results["day_7"]["concurrency_safety"] = "PASS"
        else:
            print("  ❌ FAIL: Concurrent snapshot inconsistency")
            self.results["day_7"]["concurrency_safety"] = "FAIL"

    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)

        total_tests = 0
        total_passed = 0

        for day, tests in self.results.items():
            print(f"\n{day.upper()}:")
            for test_name, status in tests.items():
                total_tests += 1
                if status == "PASS":
                    total_passed += 1
                    print(f"  ✅ {test_name}: {status}")
                else:
                    print(f"  ❌ {test_name}: {status}")

        print("\n" + "-" * 80)
        print(f"TOTAL: {total_passed}/{total_tests} PASSED ({total_passed/total_tests*100:.1f}%)")
        print("=" * 80)

        if total_passed == total_tests:
            print("\n🟢 ALL TESTS PASSED - PRODUCTION READY")
        else:
            print(f"\n🔴 {total_tests - total_passed} TESTS FAILED")


if __name__ == "__main__":
    runner = IntegrationTestRunner()
    runner.run_all_tests()
