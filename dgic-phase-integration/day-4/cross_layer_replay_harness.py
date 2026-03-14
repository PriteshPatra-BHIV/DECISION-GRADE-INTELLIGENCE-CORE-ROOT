import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any

sys.path.insert(0, str(Path(__file__).parent.parent / "day-1"))
sys.path.insert(0, str(Path(__file__).parent.parent / "day-2"))
sys.path.insert(0, str(Path(__file__).parent.parent / "day-3"))

from integration_harness import DGICIntegrationHarness
from enforcement_adapter import EnforcementAdapter
from orchestration_adapter import OrchestrationAdapter


class CrossLayerReplayHarness:
    """
    Validates deterministic replay across DGIC → Enforcement → Core pipeline.
    Ensures semantic hash equality across all layers.
    """

    def __init__(self, dgic_core):
        self.harness = DGICIntegrationHarness(dgic_core)
        self.enforcement = EnforcementAdapter(self.harness)
        self.orchestration = OrchestrationAdapter(self.harness)
        self.replay_ledger = []

    def execute_pipeline(self) -> Dict[str, Any]:
        """Execute full cross-layer pipeline and capture outputs."""
        snapshot = self.harness.generate_snapshot()
        risk_score = self.enforcement.compute_risk_score()
        decision = self.orchestration.propose_decision()

        return {
            "snapshot": snapshot.__dict__,
            "risk_score": risk_score,
            "decision": decision,
            "semantic_hash": self._compute_semantic_hash(snapshot, risk_score, decision)
        }

    def _compute_semantic_hash(self, snapshot, risk_score, decision) -> str:
        """Compute deterministic hash of entire pipeline output."""
        canonical = json.dumps({
            "snapshot": snapshot.__dict__,
            "risk_score": risk_score,
            "decision": decision
        }, sort_keys=True, separators=(',', ':'), default=str)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def replay_validation(self, iterations: int = 10000) -> Dict[str, Any]:
        """Execute pipeline N times and validate semantic hash consistency."""
        baseline = self.execute_pipeline()
        baseline_hash = baseline["semantic_hash"]
        
        mismatches = []
        for i in range(iterations):
            result = self.execute_pipeline()
            if result["semantic_hash"] != baseline_hash:
                mismatches.append({
                    "iteration": i,
                    "expected": baseline_hash,
                    "actual": result["semantic_hash"]
                })
            self.replay_ledger.append(result)

        return {
            "total_iterations": iterations,
            "baseline_hash": baseline_hash,
            "mismatches": mismatches,
            "consistency_rate": (iterations - len(mismatches)) / iterations,
            "status": "PASS" if len(mismatches) == 0 else "FAIL"
        }

    def detect_drift(self) -> Dict[str, Any]:
        """Detect if nondeterminism was injected into pipeline."""
        if len(self.replay_ledger) < 2:
            return {"status": "INSUFFICIENT_DATA"}

        hashes = [entry["semantic_hash"] for entry in self.replay_ledger]
        unique_hashes = set(hashes)

        return {
            "total_executions": len(self.replay_ledger),
            "unique_hashes": len(unique_hashes),
            "drift_detected": len(unique_hashes) > 1,
            "status": "PASS" if len(unique_hashes) == 1 else "FAIL"
        }

    def get_replay_chain(self) -> List[Dict[str, Any]]:
        """Return full replay ledger chain."""
        return self.replay_ledger


if __name__ == "__main__":
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

    core = MockDGICCore()
    harness = CrossLayerReplayHarness(core)

    print("Cross-Layer Replay Harness")
    print("=" * 60)

    result = harness.replay_validation(iterations=100)
    print(f"\nReplay Validation (100 iterations):")
    print(f"  Consistency Rate: {result['consistency_rate']:.2%}")
    print(f"  Mismatches: {len(result['mismatches'])}")
    print(f"  Status: {result['status']}")

    drift = harness.detect_drift()
    print(f"\nDrift Detection:")
    print(f"  Unique Hashes: {drift['unique_hashes']}")
    print(f"  Drift Detected: {drift['drift_detected']}")
    print(f"  Status: {drift['status']}")
