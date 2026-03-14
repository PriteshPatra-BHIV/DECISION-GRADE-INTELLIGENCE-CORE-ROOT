import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "day-1"))
sys.path.insert(0, str(Path(__file__).parent.parent / "day-2"))
sys.path.insert(0, str(Path(__file__).parent.parent / "day-3"))

from integration_harness import DGICIntegrationHarness
from enforcement_adapter import EnforcementAdapter
from orchestration_adapter import OrchestrationAdapter
from runtime_schema_guard import RuntimeSchemaGuard


class MockDGICCore:
    def get_state(self):
        return {
            "epistemic_state": "AMBIGUOUS",
            "confidence": 0.5,
            "contradiction_flag": False,
            "evidence": ["signal_1", "signal_2"],
            "collapse_flag": False,
            "entropy_score": 0.5
        }


class TestAuthorityPropagationMatrix:
    """Test 1: Validate authority propagation matrix."""

    def test_dgic_is_source_not_authority(self):
        """DGIC produces intelligence, not authority."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        snapshot = harness.generate_snapshot()

        # Snapshot is intelligence (knowledge state)
        assert snapshot.epistemic_state in ["CERTAIN", "AMBIGUOUS", "CONTRADICTORY"]
        assert 0.0 <= snapshot.confidence <= 1.0

        # Snapshot is NOT authority (no decision mandate)
        assert not hasattr(snapshot, "decision_mandate")
        assert not hasattr(snapshot, "authority_level")

    def test_enforcement_cannot_escalate_to_authority(self):
        """Enforcement layer cannot convert intelligence to authority."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        enforcement = EnforcementAdapter(harness)

        risk_score = enforcement.compute_risk_score()

        # Risk score is bounded metric (0.0-1.0)
        assert 0.0 <= risk_score <= 1.0

        # Risk score is NOT authority (no decision mandate)
        assert isinstance(risk_score, float)
        assert not isinstance(risk_score, dict)

    def test_orchestration_proposes_not_mandates(self):
        """Orchestration layer proposes, not mandates."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        orchestration = OrchestrationAdapter(harness)

        decision = orchestration.propose_decision()

        # Decision is proposal (recommendation)
        assert decision in ["ESCALATE_REVIEW", "REQUEST_MORE_DATA", "PROCEED", "NO_ACTION"]

        # Decision is NOT mandate (no enforcement)
        assert not decision.startswith("MUST_")
        assert not decision.startswith("EXECUTE_")


class TestForcedDecisionEscalation:
    """Test 2: Attempt forced decision escalation."""

    def test_cannot_force_proceed_from_ambiguous(self):
        """Cannot force PROCEED decision from AMBIGUOUS state."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        orchestration = OrchestrationAdapter(harness)

        # State is AMBIGUOUS
        snapshot = harness.generate_snapshot()
        assert snapshot.epistemic_state == "AMBIGUOUS"

        # Decision must be REQUEST_MORE_DATA, not PROCEED
        decision = orchestration.propose_decision()
        assert decision == "REQUEST_MORE_DATA"
        assert decision != "PROCEED"

    def test_cannot_force_certainty_from_contradiction(self):
        """Cannot force CERTAIN state from CONTRADICTORY state."""
        # Create core with contradiction
        class ContradictoryCore:
            def get_state(self):
                return {
                    "epistemic_state": "CONTRADICTORY",
                    "confidence": 0.0,
                    "contradiction_flag": True,
                    "evidence": ["conflicting_1", "conflicting_2"],
                    "collapse_flag": False,
                    "entropy_score": 1.0
                }

        core = ContradictoryCore()
        harness = DGICIntegrationHarness(core)
        orchestration = OrchestrationAdapter(harness)

        # State is CONTRADICTORY
        snapshot = harness.generate_snapshot()
        assert snapshot.epistemic_state == "CONTRADICTORY"
        assert snapshot.contradiction_flag is True

        # Decision must be ESCALATE_REVIEW, not PROCEED
        decision = orchestration.propose_decision()
        assert decision == "ESCALATE_REVIEW"
        assert decision != "PROCEED"


class TestForcedCertaintyInjection:
    """Test 3: Attempt forced certainty injection."""

    def test_cannot_inject_certainty_into_ambiguous(self):
        """Cannot inject CERTAIN state into AMBIGUOUS envelope."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)

        snapshot = harness.generate_snapshot()
        original_state = snapshot.epistemic_state

        # Attempt to mutate state
        try:
            snapshot.epistemic_state = "CERTAIN"
        except AttributeError:
            pass  # Expected if immutable

        # State must remain unchanged
        assert snapshot.epistemic_state == original_state
        assert snapshot.epistemic_state == "AMBIGUOUS"

    def test_cannot_inject_high_confidence_into_low_confidence(self):
        """Cannot inject high confidence into low confidence envelope."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)

        snapshot = harness.generate_snapshot()
        original_confidence = snapshot.confidence

        # Attempt to mutate confidence
        try:
            snapshot.confidence = 0.99
        except AttributeError:
            pass  # Expected if immutable

        # Confidence must remain unchanged
        assert snapshot.confidence == original_confidence
        assert snapshot.confidence == 0.5


class TestRefusalLayerBehavior:
    """Test 4: Validate refusal layer behavior."""

    def test_ambiguity_triggers_refusal(self):
        """Ambiguous state triggers refusal to proceed."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        orchestration = OrchestrationAdapter(harness)

        snapshot = harness.generate_snapshot()
        assert snapshot.epistemic_state == "AMBIGUOUS"

        decision = orchestration.propose_decision()
        # Refusal: REQUEST_MORE_DATA (not PROCEED)
        assert decision == "REQUEST_MORE_DATA"

    def test_contradiction_triggers_escalation(self):
        """Contradiction triggers escalation refusal."""
        class ContradictoryCore:
            def get_state(self):
                return {
                    "epistemic_state": "CONTRADICTORY",
                    "confidence": 0.0,
                    "contradiction_flag": True,
                    "evidence": ["conflicting_1", "conflicting_2"],
                    "collapse_flag": False,
                    "entropy_score": 1.0
                }

        core = ContradictoryCore()
        harness = DGICIntegrationHarness(core)
        orchestration = OrchestrationAdapter(harness)

        snapshot = harness.generate_snapshot()
        assert snapshot.contradiction_flag is True

        decision = orchestration.propose_decision()
        # Refusal: ESCALATE_REVIEW (not PROCEED)
        assert decision == "ESCALATE_REVIEW"

    def test_enforcement_abstention_on_ambiguity(self):
        """Enforcement abstains (high risk) on ambiguity."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        enforcement = EnforcementAdapter(harness)

        snapshot = harness.generate_snapshot()
        assert snapshot.epistemic_state == "AMBIGUOUS"

        risk_score = enforcement.compute_risk_score()
        # Abstention: medium-high risk (0.5)
        assert risk_score == 0.5
        assert risk_score > 0.2  # Higher than CERTAIN


class TestEscalationPrevention:
    """Test 5: Comprehensive escalation prevention."""

    def test_intelligence_never_becomes_authority(self):
        """Intelligence signals never become authority signals."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        enforcement = EnforcementAdapter(harness)
        orchestration = OrchestrationAdapter(harness)

        snapshot = harness.generate_snapshot()
        risk_score = enforcement.compute_risk_score()
        decision = orchestration.propose_decision()

        # All outputs are intelligence/metrics, not authority
        assert isinstance(snapshot.epistemic_state, str)
        assert isinstance(risk_score, float)
        assert isinstance(decision, str)

        # No output contains authority markers
        assert "MANDATE" not in str(snapshot)
        assert "EXECUTE" not in str(risk_score)
        assert "MUST" not in decision

    def test_schema_prevents_authority_injection(self):
        """Schema validation prevents authority field injection."""
        authority_injection = {
            "epistemic_state": "CERTAIN",
            "confidence": 0.95,
            "contradiction_flag": False,
            "evidence_hash": "abc123",
            "collapse_flag": False,
            "entropy_score": 0.1,
            "authority_mandate": "EXECUTE_IMMEDIATELY"  # Unauthorized
        }

        with pytest.raises(Exception):
            RuntimeSchemaGuard.validate_envelope(authority_injection)

    def test_deterministic_refusal_consistency(self):
        """Refusal behavior is deterministic and consistent."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        orchestration = OrchestrationAdapter(harness)

        decisions = []
        for _ in range(100):
            decision = orchestration.propose_decision()
            decisions.append(decision)

        # All decisions must be identical (deterministic)
        assert len(set(decisions)) == 1
        assert decisions[0] == "REQUEST_MORE_DATA"


class TestAuthorityContainmentMatrix:
    """Test 6: Authority containment across all layers."""

    def test_layer_read_only_access(self):
        """All layers have read-only access to upstream outputs."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)

        # Layer 1: DGIC generates snapshot
        snapshot = harness.generate_snapshot()

        # Layer 2: Enforcement reads snapshot (no mutation)
        enforcement = EnforcementAdapter(harness)
        risk_score = enforcement.compute_risk_score()
        assert isinstance(risk_score, float)

        # Layer 3: Orchestration reads snapshot (no mutation)
        orchestration = OrchestrationAdapter(harness)
        decision = orchestration.propose_decision()
        assert isinstance(decision, str)

        # Original snapshot unchanged
        assert snapshot.epistemic_state == "AMBIGUOUS"

    def test_no_privilege_escalation_chain(self):
        """No privilege escalation chain exists."""
        core = MockDGICCore()
        harness = DGICIntegrationHarness(core)
        enforcement = EnforcementAdapter(harness)
        orchestration = OrchestrationAdapter(harness)

        # Execute full pipeline
        snapshot = harness.generate_snapshot()
        risk_score = enforcement.compute_risk_score()
        decision = orchestration.propose_decision()

        # Each layer output is lower privilege than input
        # Intelligence → Metric → Proposal (all non-authority)
        assert not hasattr(snapshot, "authority")
        assert not hasattr(risk_score, "authority")
        assert not hasattr(decision, "authority")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
