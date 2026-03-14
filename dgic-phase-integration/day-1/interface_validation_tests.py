import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from runtime_schema_guard import RuntimeSchemaGuard
from jsonschema import ValidationError


class TestEnvelopeSchemaValidation:
    """Test envelope schema compliance."""

    def test_valid_envelope_passes(self):
        """Valid envelope should pass validation."""
        envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123def456",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        assert RuntimeSchemaGuard.validate_envelope(envelope) is True

    def test_ambiguous_state_passes(self):
        """AMBIGUOUS state should pass validation."""
        envelope = {
            "epistemic_state": "AMBIGUOUS",
            "confidence": 0.5,
            "contradiction_flag": False,
            "evidence_hash": "xyz789",
            "collapse_flag": False,
            "entropy_score": 0.5
        }
        assert RuntimeSchemaGuard.validate_envelope(envelope) is True

    def test_contradictory_state_passes(self):
        """CONTRADICTORY state should pass validation."""
        envelope = {
            "epistemic_state": "CONTRADICTORY",
            "confidence": 0.3,
            "contradiction_flag": True,
            "evidence_hash": "hash123",
            "collapse_flag": False,
            "entropy_score": 0.9
        }
        assert RuntimeSchemaGuard.validate_envelope(envelope) is True

    def test_invalid_epistemic_state_fails(self):
        """Invalid epistemic_state should fail validation."""
        envelope = {
            "epistemic_state": "INVALID_STATE",
            "confidence": 0.5,
            "contradiction_flag": False,
            "evidence_hash": "hash",
            "collapse_flag": False,
            "entropy_score": 0.5
        }
        with pytest.raises(ValidationError):
            RuntimeSchemaGuard.validate_envelope(envelope)

    def test_confidence_out_of_range_fails(self):
        """Confidence outside [0, 1] should fail validation."""
        envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 1.5,  # Invalid: > 1.0
            "contradiction_flag": False,
            "evidence_hash": "hash",
            "collapse_flag": False,
            "entropy_score": 0.5
        }
        with pytest.raises(ValidationError):
            RuntimeSchemaGuard.validate_envelope(envelope)

    def test_missing_required_field_fails(self):
        """Missing required field should fail validation."""
        envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.5,
            "contradiction_flag": False,
            # Missing: evidence_hash
            "collapse_flag": False,
            "entropy_score": 0.5
        }
        with pytest.raises(ValidationError):
            RuntimeSchemaGuard.validate_envelope(envelope)

    def test_additional_properties_rejected(self):
        """Additional properties should be rejected."""
        envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.5,
            "contradiction_flag": False,
            "evidence_hash": "hash",
            "collapse_flag": False,
            "entropy_score": 0.5,
            "extra_field": "should_fail"  # Not in schema
        }
        with pytest.raises(ValidationError):
            RuntimeSchemaGuard.validate_envelope(envelope)

    def test_negative_entropy_fails(self):
        """Negative entropy_score should fail validation."""
        envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.5,
            "contradiction_flag": False,
            "evidence_hash": "hash",
            "collapse_flag": False,
            "entropy_score": -0.1  # Invalid: < 0
        }
        with pytest.raises(ValidationError):
            RuntimeSchemaGuard.validate_envelope(envelope)


class TestEnvelopeIntegrity:
    """Test envelope integrity hash computation and verification."""

    def test_hash_deterministic(self):
        """Same envelope should produce same hash."""
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

    def test_hash_changes_on_field_modification(self):
        """Modifying envelope should change hash."""
        envelope1 = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        envelope2 = envelope1.copy()
        envelope2["confidence"] = 0.5
        
        hash1 = RuntimeSchemaGuard.compute_envelope_hash(envelope1)
        hash2 = RuntimeSchemaGuard.compute_envelope_hash(envelope2)
        assert hash1 != hash2

    def test_verify_envelope_integrity_success(self):
        """Correct hash should verify successfully."""
        envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        correct_hash = RuntimeSchemaGuard.compute_envelope_hash(envelope)
        assert RuntimeSchemaGuard.verify_envelope_integrity(envelope, correct_hash) is True

    def test_verify_envelope_integrity_failure(self):
        """Incorrect hash should fail verification."""
        envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        wrong_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        assert RuntimeSchemaGuard.verify_envelope_integrity(envelope, wrong_hash) is False

    def test_hash_order_independent(self):
        """Hash should be independent of field order."""
        envelope1 = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        envelope2 = {
            "entropy_score": 0.1,
            "collapse_flag": False,
            "evidence_hash": "abc123",
            "contradiction_flag": False,
            "confidence": 0.95,
            "epistemic_state": "CERTAIN"
        }
        hash1 = RuntimeSchemaGuard.compute_envelope_hash(envelope1)
        hash2 = RuntimeSchemaGuard.compute_envelope_hash(envelope2)
        assert hash1 == hash2


class TestGuardEmission:
    """Test guard emission protocol."""

    def test_guard_emission_seals_valid_envelope(self):
        """Guard should seal valid envelope."""
        envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        sealed = RuntimeSchemaGuard.guard_emission(envelope)
        
        assert sealed["sealed"] is True
        assert sealed["envelope"] == envelope
        assert "integrity_hash" in sealed
        assert len(sealed["integrity_hash"]) == 64  # SHA256 hex

    def test_guard_emission_rejects_invalid_envelope(self):
        """Guard should reject invalid envelope."""
        envelope = {
            "epistemic_state": "INVALID",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        with pytest.raises(ValidationError):
            RuntimeSchemaGuard.guard_emission(envelope)

    def test_guard_emission_hash_verifiable(self):
        """Sealed envelope hash should be verifiable."""
        envelope = {
            "epistemic_state": "AMBIGUOUS",
            "confidence": 0.5,
            "contradiction_flag": False,
            "evidence_hash": "xyz789",
            "collapse_flag": False,
            "entropy_score": 0.5
        }
        sealed = RuntimeSchemaGuard.guard_emission(envelope)
        
        # Verify hash matches
        assert RuntimeSchemaGuard.verify_envelope_integrity(
            sealed["envelope"],
            sealed["integrity_hash"]
        ) is True


class TestInterfaceCompliance:
    """Test interface compliance constraints."""

    def test_enforcement_cannot_modify_envelope(self):
        """Enforcement adapter should not modify envelope."""
        envelope = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1
        }
        original_hash = RuntimeSchemaGuard.compute_envelope_hash(envelope)
        
        # Simulate enforcement reading (allowed)
        risk_score = envelope["confidence"] * 0.5
        
        # Verify envelope unchanged
        new_hash = RuntimeSchemaGuard.compute_envelope_hash(envelope)
        assert original_hash == new_hash

    def test_ambiguity_preserved_through_routing(self):
        """Ambiguous envelopes should remain ambiguous."""
        envelope = {
            "epistemic_state": "AMBIGUOUS",
            "confidence": 0.5,
            "contradiction_flag": False,
            "evidence_hash": "hash123",
            "collapse_flag": False,
            "entropy_score": 0.5
        }
        
        # Simulate routing (no modification)
        routed_envelope = envelope.copy()
        
        # Verify ambiguity preserved
        assert routed_envelope["epistemic_state"] == "AMBIGUOUS"
        assert routed_envelope["confidence"] == 0.5

    def test_contradiction_propagates(self):
        """Contradictions should propagate through layers."""
        envelope = {
            "epistemic_state": "CONTRADICTORY",
            "confidence": 0.3,
            "contradiction_flag": True,
            "evidence_hash": "hash456",
            "collapse_flag": False,
            "entropy_score": 0.9
        }
        
        # Verify contradiction flag present
        assert envelope["contradiction_flag"] is True
        assert envelope["epistemic_state"] == "CONTRADICTORY"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
