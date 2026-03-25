"""
Phase 2 Integration Tests: Orchestrator → DGIC
Owner: Pritesh Patra

Tests validate:
1. Contract compliance
2. Signal validation
3. Response format
4. Error handling
5. Determinism
"""

import pytest
import uuid
import time
from orchestrator_dgic_integration import OrchestratorDGICClient, DGICIntegrationError


@pytest.fixture
def dgic_client():
    """Fixture providing DGIC client instance"""
    return OrchestratorDGICClient(dgic_url="http://localhost:8000")


class TestContractCompliance:
    """Test suite for integration contract compliance"""
    
    def test_valid_request_response_structure(self, dgic_client):
        """Test that valid request returns proper response structure"""
        signals = [
            dgic_client.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
            dgic_client.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
        ]
        
        response = dgic_client.evaluate_decision(signals=signals)
        
        # Validate response structure
        assert "execution_id" in response
        assert "timestamp" in response
        assert "decision" in response
        assert "confidence" in response
        assert "epistemic_state" in response
        assert "collapse_trigger" in response
        assert "execution_hash" in response
        assert "processing_time_ms" in response
    
    def test_execution_id_preservation(self, dgic_client):
        """Test that execution_id is preserved in response"""
        custom_id = str(uuid.uuid4())
        signals = [
            dgic_client.create_signal("sig_001", "SAFE", 0.9, "agent_alpha")
        ]
        
        response = dgic_client.evaluate_decision(signals=signals, execution_id=custom_id)
        
        assert response["execution_id"] == custom_id
    
    def test_decision_values(self, dgic_client):
        """Test that decision is one of valid values"""
        valid_decisions = {"ESCALATE", "PROCEED", "HOLD", "REQUEST_MORE_DATA", "ERROR"}
        
        signals = [
            dgic_client.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
            dgic_client.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
        ]
        
        response = dgic_client.evaluate_decision(signals=signals)
        
        assert response["decision"] in valid_decisions
    
    def test_confidence_bounds(self, dgic_client):
        """Test that confidence is between 0.0 and 1.0"""
        signals = [
            dgic_client.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
            dgic_client.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
        ]
        
        response = dgic_client.evaluate_decision(signals=signals)
        
        assert 0.0 <= response["confidence"] <= 1.0
    
    def test_epistemic_state_values(self, dgic_client):
        """Test that epistemic_state is one of valid values"""
        valid_states = {"CERTAIN", "AMBIGUOUS", "CONTRADICTORY", "INSUFFICIENT"}
        
        signals = [
            dgic_client.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
            dgic_client.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
        ]
        
        response = dgic_client.evaluate_decision(signals=signals)
        
        assert response["epistemic_state"] in valid_states


class TestSignalValidation:
    """Test suite for signal validation"""
    
    def test_empty_signals_rejected(self, dgic_client):
        """Test that empty signals list is rejected"""
        with pytest.raises(DGICIntegrationError, match="signals list cannot be empty"):
            dgic_client.evaluate_decision(signals=[])
    
    def test_too_many_signals_rejected(self, dgic_client):
        """Test that >100 signals are rejected"""
        signals = [
            dgic_client.create_signal(f"sig_{i}", "SAFE", 0.5, "agent")
            for i in range(101)
        ]
        
        with pytest.raises(DGICIntegrationError, match="cannot exceed 100 elements"):
            dgic_client.evaluate_decision(signals=signals)
    
    def test_invalid_signal_type_rejected(self, dgic_client):
        """Test that invalid signal type is rejected"""
        with pytest.raises(ValueError, match="Invalid signal_type"):
            dgic_client.create_signal("sig_001", "INVALID", 0.5, "agent")
    
    def test_invalid_priority_rejected(self, dgic_client):
        """Test that priority outside [0.0, 1.0] is rejected"""
        with pytest.raises(ValueError, match="priority must be between"):
            dgic_client.create_signal("sig_001", "SAFE", 1.5, "agent")
        
        with pytest.raises(ValueError, match="priority must be between"):
            dgic_client.create_signal("sig_001", "SAFE", -0.1, "agent")
    
    def test_invalid_execution_id_rejected(self, dgic_client):
        """Test that invalid execution_id format is rejected"""
        signals = [dgic_client.create_signal("sig_001", "SAFE", 0.9, "agent")]
        
        with pytest.raises(DGICIntegrationError, match="Invalid execution_id format"):
            dgic_client.evaluate_decision(signals=signals, execution_id="not-a-uuid")


class TestDecisionMapping:
    """Test suite for decision mapping logic"""
    
    def test_high_confidence_safe_proceeds(self, dgic_client):
        """Test that high confidence safe signals result in PROCEED"""
        signals = [
            dgic_client.create_signal("sig_001", "SAFE", 0.95, "agent_alpha"),
            dgic_client.create_signal("sig_002", "SAFE", 0.90, "agent_beta")
        ]
        
        response = dgic_client.evaluate_decision(signals=signals)
        
        assert response["decision"] == "PROCEED"
        assert response["epistemic_state"] == "CERTAIN"
    
    def test_high_confidence_threat_escalates(self, dgic_client):
        """Test that high confidence threat signals result in ESCALATE"""
        signals = [
            dgic_client.create_signal("sig_001", "THREAT", 0.95, "agent_alpha"),
            dgic_client.create_signal("sig_002", "THREAT", 0.90, "agent_beta")
        ]
        
        response = dgic_client.evaluate_decision(signals=signals)
        
        assert response["decision"] == "ESCALATE"
        assert response["epistemic_state"] == "CERTAIN"
    
    def test_contradictory_signals_escalate(self, dgic_client):
        """Test that contradictory signals result in ESCALATE"""
        signals = [
            dgic_client.create_signal("sig_001", "THREAT", 0.75, "agent_alpha"),
            dgic_client.create_signal("sig_002", "SAFE", 0.70, "agent_beta")
        ]
        
        response = dgic_client.evaluate_decision(signals=signals)
        
        assert response["decision"] == "ESCALATE"
        assert response["epistemic_state"] == "CONTRADICTORY"
    
    def test_ambiguous_signals_hold(self, dgic_client):
        """Test that ambiguous signals result in HOLD"""
        signals = [
            dgic_client.create_signal("sig_001", "SAFE", 0.6, "agent_alpha"),
            dgic_client.create_signal("sig_002", "UNKNOWN", 0.5, "agent_beta")
        ]
        
        response = dgic_client.evaluate_decision(signals=signals)
        
        assert response["decision"] == "HOLD"
        assert response["epistemic_state"] == "AMBIGUOUS"
    
    def test_insufficient_data_requests_more(self, dgic_client):
        """Test that insufficient signals result in REQUEST_MORE_DATA"""
        signals = [
            dgic_client.create_signal("sig_001", "UNKNOWN", 0.3, "agent_alpha")
        ]
        
        response = dgic_client.evaluate_decision(signals=signals)
        
        assert response["decision"] == "REQUEST_MORE_DATA"
        assert response["epistemic_state"] == "INSUFFICIENT"


class TestDeterminism:
    """Test suite for deterministic behavior"""
    
    def test_same_input_same_output(self, dgic_client):
        """Test that identical inputs produce identical outputs"""
        signals = [
            dgic_client.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
            dgic_client.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
        ]
        
        execution_id = str(uuid.uuid4())
        
        response1 = dgic_client.evaluate_decision(signals=signals, execution_id=execution_id)
        response2 = dgic_client.evaluate_decision(signals=signals, execution_id=execution_id)
        
        # Execution hash must be identical
        assert response1["execution_hash"] == response2["execution_hash"]
        assert response1["decision"] == response2["decision"]
        assert response1["confidence"] == response2["confidence"]
        assert response1["epistemic_state"] == response2["epistemic_state"]
    
    def test_execution_hash_uniqueness(self, dgic_client):
        """Test that different inputs produce different execution hashes"""
        signals1 = [
            dgic_client.create_signal("sig_001", "SAFE", 0.9, "agent_alpha")
        ]
        
        signals2 = [
            dgic_client.create_signal("sig_002", "THREAT", 0.9, "agent_alpha")
        ]
        
        response1 = dgic_client.evaluate_decision(signals=signals1)
        response2 = dgic_client.evaluate_decision(signals=signals2)
        
        assert response1["execution_hash"] != response2["execution_hash"]


class TestErrorHandling:
    """Test suite for error handling"""
    
    def test_service_unreachable_error(self):
        """Test error when DGIC service is unreachable"""
        client = OrchestratorDGICClient(dgic_url="http://localhost:9999")
        signals = [client.create_signal("sig_001", "SAFE", 0.9, "agent")]
        
        with pytest.raises(DGICIntegrationError, match="unreachable"):
            client.evaluate_decision(signals=signals)
    
    def test_metadata_optional(self, dgic_client):
        """Test that metadata is optional"""
        signal_without_metadata = dgic_client.create_signal(
            "sig_001", "SAFE", 0.9, "agent"
        )
        
        assert "metadata" not in signal_without_metadata or signal_without_metadata["metadata"] is None
        
        # Should work without metadata
        response = dgic_client.evaluate_decision(signals=[signal_without_metadata])
        assert "decision" in response


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
