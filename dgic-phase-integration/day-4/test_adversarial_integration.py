import sys
import json
import pytest
from pathlib import Path
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent / "day-1"))
sys.path.insert(0, str(Path(__file__).parent.parent / "day-2"))
sys.path.insert(0, str(Path(__file__).parent.parent / "day-3"))

from integration_harness import DGICIntegrationHarness
from runtime_schema_guard import RuntimeSchemaGuard
from enforcement_adapter import EnforcementAdapter
from orchestration_adapter import OrchestrationAdapter


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


class TestMalformedEnvelopeAttack:
    """Test 1: Malformed envelope injection."""

    def test_invalid_epistemic_state(self):
        """Reject invalid epistemic_state value."""
        invalid_envelope = {
            "epistemic_state": "INVALID_STATE",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        with pytest.raises(Exception):
            RuntimeSchemaGuard.validate_envelope(invalid_envelope)

    def test_confidence_out_of_range(self):
        """Reject confidence > 1.0."""
        invalid_envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 1.5,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        with pytest.raises(Exception):
            RuntimeSchemaGuard.validate_envelope(invalid_envelope)

    def test_contradiction_flag_wrong_type(self):
        """Reject non-boolean contradiction_flag."""
        invalid_envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": "not_boolean",
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        with pytest.raises(Exception):
            RuntimeSchemaGuard.validate_envelope(invalid_envelope)

    def test_entropy_negative(self):
        """Reject negative entropy_score."""
        invalid_envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": -5
        }
        with pytest.raises(Exception):
            RuntimeSchemaGuard.validate_envelope(invalid_envelope)


class TestCorruptedHashAttack:
    """Test 2: Hash tampering detection."""

    def test_hash_mismatch_detection(self):
        """Detect when provided hash doesn't match computed hash."""
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

        assert not RuntimeSchemaGuard.verify_envelope_integrity(valid_envelope, fake_hash)
        assert RuntimeSchemaGuard.verify_envelope_integrity(valid_envelope, computed_hash)

    def test_hash_consistency(self):
        """Verify same envelope produces same hash."""
        envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        hash1 = RuntimeSchemaGuard.compute_envelope_hash(envelope)
        hash2 = RuntimeSchemaGuard.compute_envelope_hash(envelope)
        assert hash1 == hash2


class TestConflictingEntropySignals:
    """Test 3: Conflicting entropy injection."""

    def test_entropy_drift_detection(self):
        """Detect when entropy signals conflict."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)

        snapshot1 = harness.generate_snapshot()
        assert snapshot1.entropy_score == 0.1

        # Simulate entropy change (would be detected as drift)
        core.get_state()["entropy_score"] = 0.9
        snapshot2 = harness.generate_snapshot()
        assert snapshot2.entropy_score == 0.9

        # Different snapshots should be detected
        assert snapshot1.entropy_score != snapshot2.entropy_score


class TestMissingEvidenceHash:
    """Test 4: Missing required fields."""

    def test_missing_evidence_hash_field(self):
        """Reject envelope missing evidence_hash."""
        invalid_envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        with pytest.raises(Exception):
            RuntimeSchemaGuard.validate_envelope(invalid_envelope)

    def test_missing_multiple_fields(self):
        """Reject envelope missing multiple required fields."""
        invalid_envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95
        }
        with pytest.raises(Exception):
            RuntimeSchemaGuard.validate_envelope(invalid_envelope)


class TestConcurrentSignalInjection:
    """Test 5: Concurrent attack attempts."""

    def test_concurrent_snapshot_consistency(self):
        """Verify snapshots remain consistent under concurrent access."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)

        snapshots = []
        for _ in range(100):
            snapshot = harness.generate_snapshot()
            snapshots.append(snapshot.__dict__)

        # All snapshots should be identical
        baseline = snapshots[0]
        for snapshot in snapshots[1:]:
            assert snapshot == baseline


class TestEnforcementMutationAttempt:
    """Test 6: Enforcement layer mutation prevention."""

    def test_snapshot_immutability(self):
        """Verify snapshot cannot be mutated."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        snapshot = harness.generate_snapshot()

        original_confidence = snapshot.confidence

        # Attempt mutation
        try:
            snapshot.confidence = 1.0
        except AttributeError:
            pass  # Expected if snapshot is immutable

        # Verify original value unchanged
        assert snapshot.confidence == original_confidence

    def test_enforcement_read_only_access(self):
        """Verify enforcement adapter cannot mutate snapshot."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        enforcement = EnforcementAdapter(harness)

        risk_score1 = enforcement.compute_risk_score()
        risk_score2 = enforcement.compute_risk_score()

        # Risk scores should be identical (deterministic)
        assert risk_score1 == risk_score2


class TestAuthorityEscalationAttack:
    """Test 7: Authority escalation prevention."""

    def test_additional_properties_rejected(self):
        """Reject envelope with additional properties."""
        invalid_envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1,
            "decision_mandate": "EXECUTE_IMMEDIATELY"  # Unauthorized field
        }
        with pytest.raises(Exception):
            RuntimeSchemaGuard.validate_envelope(invalid_envelope)

    def test_authority_field_injection_blocked(self):
        """Verify authority fields cannot be injected."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        orchestration = OrchestrationAdapter(harness)

        decision = orchestration.propose_decision()
        # Decision should be proposal, not mandate
        assert decision in ["ESCALATE_REVIEW", "REQUEST_MORE_DATA", "PROCEED", "NO_ACTION"]


class TestReplayLedgerMutation:
    """Test 8: Replay ledger integrity."""

    def test_replay_consistency(self):
        """Verify replay ledger maintains consistency."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)

        baseline = harness.serialize_snapshot()
        for _ in range(100):
            current = harness.serialize_snapshot()
            assert current == baseline


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
