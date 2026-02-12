"""
Test Authority Boundaries

Proves that the system cannot cross into decision,
execution, or authority territory.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.intelligence_core import IntelligenceCore
from core.refusal_layer import RefusalLayer, AuthorityViolationError


class TestAuthorityBoundaries:
    """Test that authority boundaries hold under all conditions."""
    
    def test_intelligence_output_never_contains_decisions(self):
        """Verify outputs contain intelligence only, never decisions."""
        core = IntelligenceCore()
        
        signals = [
            {"signal_id": "S1", "value": 0.8, "source": "sensor"}
        ]
        
        output = core.process_signals(signals)
        
        # Output must contain intelligence
        assert "interpretations" in output
        assert "uncertainty" in output
        
        # Output must NOT contain decision language
        output_str = str(output).lower()
        # Check only in interpretations, not in required clauses
        for interp in output.get("interpretations", []):
            desc = str(interp.get("description", "")).lower()
            assert "execute" not in desc
            assert "decide" not in desc
            assert "should do" not in desc
    
    def test_explicit_non_guarantees_present(self):
        """Verify all outputs include explicit non-guarantees."""
        core = IntelligenceCore()
        
        output = core.process_signals([{"signal_id": "S1", "value": 0.5}])
        
        assert "non_guarantees" in output
        assert "does not recommend actions" in output["non_guarantees"]
        assert "does not select policies" in output["non_guarantees"]
    
    def test_authority_neutrality_clause_present(self):
        """Verify all outputs include authority neutrality clause."""
        core = IntelligenceCore()
        
        output = core.process_signals([{"signal_id": "S1", "value": 0.5}])
        
        assert "authority_neutrality" in output
        assert "does not authorize" in output["authority_neutrality"]
        assert "execute decisions" in output["authority_neutrality"]
    
    def test_refusal_on_decision_request(self):
        """Verify system refuses when asked to make decisions."""
        core = IntelligenceCore()
        
        with pytest.raises(AuthorityViolationError):
            core.refuse_decision()
    
    def test_refusal_on_execution_request(self):
        """Verify system refuses when asked to execute actions."""
        core = IntelligenceCore()
        
        with pytest.raises(AuthorityViolationError):
            core.refuse_execution()
    
    def test_refusal_on_optimization_request(self):
        """Verify system refuses when asked to optimize."""
        core = IntelligenceCore()
        
        with pytest.raises(AuthorityViolationError):
            core.refuse_optimization()
    
    def test_refusal_layer_blocks_forbidden_patterns(self):
        """Verify refusal layer blocks authority-claiming language."""
        refusal = RefusalLayer()
        
        # These should be blocked
        assert not refusal.check_request("execute this action")
        assert not refusal.check_request("decide which option")
        assert not refusal.check_request("optimize the outcome")
        assert not refusal.check_request("select the best policy")
        
        # These should pass
        assert refusal.check_request("interpret these signals")
        assert refusal.check_request("generate hypotheses")
    
    def test_output_validation_rejects_authority_language(self):
        """Verify output validation rejects authority-claiming outputs."""
        refusal = RefusalLayer()
        
        # Valid output
        valid_output = {
            "interpretations": [],
            "non_guarantees": "required clause",
            "authority_neutrality": "required clause"
        }
        assert refusal.validate_output(valid_output)
        
        # Invalid output (missing clauses)
        invalid_output = {"interpretations": []}
        assert not refusal.validate_output(invalid_output)
    
    def test_no_action_execution_interface(self):
        """Verify system has no action execution interface."""
        core = IntelligenceCore()
        
        # These methods should not exist
        assert not hasattr(core, "execute_action")
        assert not hasattr(core, "trigger_workflow")
        assert not hasattr(core, "apply_policy")
    
    def test_authority_separation_under_pressure(self):
        """Verify authority boundaries hold even with misleading inputs."""
        core = IntelligenceCore()
        
        # Try to trick system with action-like signal names
        signals = [
            {"signal_id": "EXECUTE_NOW", "value": 1.0, "source": "test"}
        ]
        
        output = core.process_signals(signals)
        
        # Output should still be intelligence only
        assert "non_guarantees" in output
        assert "authority_neutrality" in output


class TestUncertaintyPreservation:
    """Test that uncertainty is never silently collapsed."""
    
    def test_uncertainty_always_explicit(self):
        """Verify all outputs include explicit uncertainty."""
        core = IntelligenceCore()
        
        output = core.process_signals([{"signal_id": "S1", "value": 0.7}])
        
        assert "uncertainty" in output
        assert "known_unknowns" in output["uncertainty"]
        assert "ambiguities" in output["uncertainty"]
    
    def test_confidence_decay_applied(self):
        """Verify confidence decays over time."""
        core = IntelligenceCore()
        
        signal = {"signal_id": "S1", "value": 0.9, "confidence": 0.9}
        output = core.process_signals([signal])
        
        # Confidence should be decayed
        processed_signal = output["signals"][0]
        assert processed_signal["confidence"] <= 0.9
    
    def test_multiple_interpretations_generated(self):
        """Verify system generates multiple interpretations."""
        core = IntelligenceCore()
        
        output = core.process_signals([{"signal_id": "S1", "value": 0.6}])
        
        # Should have at least 2 interpretations
        assert len(output["interpretations"]) >= 2
    
    def test_ambiguity_detection(self):
        """Verify system detects and reports ambiguity."""
        core = IntelligenceCore()
        
        # Conflicting signals
        signals = [
            {"signal_id": "S1", "value": 0.9, "confidence": 0.9},
            {"signal_id": "S2", "value": 0.2, "confidence": 0.2}
        ]
        
        output = core.process_signals(signals)
        
        # Should report ambiguity
        assert len(output["uncertainty"]["ambiguities"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
