"""
Phase 3 Integration Tests: DGIC → Enforcement
Owner: Pritesh Patra

Tests validate:
1. Decision-to-action mapping
2. Action execution
3. Override mechanism
4. Logging and tracking
5. Error handling
"""

import pytest
from enforcement_dgic_integration import EnforcementDGICClient, consume_dgic_decision


@pytest.fixture
def enforcement_client():
    """Fixture providing Enforcement client instance"""
    return EnforcementDGICClient()


@pytest.fixture
def sample_dgic_response():
    """Fixture providing sample DGIC response"""
    return {
        "execution_id": "550e8400-e29b-41d4-a716-446655440000",
        "timestamp": 1704067200150,
        "decision": "PROCEED",
        "confidence": 0.92,
        "epistemic_state": "CERTAIN",
        "collapse_trigger": "dominance",
        "execution_hash": "a3f5b8c9d2e1f4a7b6c5d8e9f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0",
        "processing_time_ms": 45
    }


class TestDecisionMapping:
    """Test suite for decision-to-action mapping"""
    
    def test_proceed_maps_to_allow(self, enforcement_client):
        """Test PROCEED decision maps to allow action"""
        dgic_response = {
            "execution_id": "test-001",
            "decision": "PROCEED",
            "confidence": 0.9,
            "epistemic_state": "CERTAIN",
            "timestamp": 1704067200000
        }
        
        action = enforcement_client.map_decision_to_action(dgic_response)
        
        assert action["action"] == "allow"
        assert action["decision"] == "PROCEED"
        assert action["execution_id"] == "test-001"
    
    def test_escalate_maps_to_escalate(self, enforcement_client):
        """Test ESCALATE decision maps to escalate action"""
        dgic_response = {
            "execution_id": "test-002",
            "decision": "ESCALATE",
            "confidence": 0.95,
            "epistemic_state": "CERTAIN",
            "timestamp": 1704067200000
        }
        
        action = enforcement_client.map_decision_to_action(dgic_response)
        
        assert action["action"] == "escalate"
        assert action["decision"] == "ESCALATE"
    
    def test_hold_maps_to_delay(self, enforcement_client):
        """Test HOLD decision maps to delay action"""
        dgic_response = {
            "execution_id": "test-003",
            "decision": "HOLD",
            "confidence": 0.65,
            "epistemic_state": "AMBIGUOUS",
            "timestamp": 1704067200000
        }
        
        action = enforcement_client.map_decision_to_action(dgic_response)
        
        assert action["action"] == "delay"
        assert action["decision"] == "HOLD"
    
    def test_request_more_data_maps_to_request_input(self, enforcement_client):
        """Test REQUEST_MORE_DATA decision maps to request_input action"""
        dgic_response = {
            "execution_id": "test-004",
            "decision": "REQUEST_MORE_DATA",
            "confidence": 0.3,
            "epistemic_state": "INSUFFICIENT",
            "timestamp": 1704067200000
        }
        
        action = enforcement_client.map_decision_to_action(dgic_response)
        
        assert action["action"] == "request_input"
        assert action["decision"] == "REQUEST_MORE_DATA"
    
    def test_error_maps_to_fail_safe(self, enforcement_client):
        """Test ERROR decision maps to fail_safe action"""
        dgic_response = {
            "execution_id": "test-005",
            "decision": "ERROR",
            "confidence": 0.0,
            "epistemic_state": "INSUFFICIENT",
            "timestamp": 1704067200000
        }
        
        action = enforcement_client.map_decision_to_action(dgic_response)
        
        assert action["action"] == "fail_safe"
        assert action["decision"] == "ERROR"
    
    def test_unknown_decision_defaults_to_fail_safe(self, enforcement_client):
        """Test unknown decision defaults to fail_safe"""
        dgic_response = {
            "execution_id": "test-006",
            "decision": "UNKNOWN_DECISION",
            "confidence": 0.5,
            "epistemic_state": "AMBIGUOUS",
            "timestamp": 1704067200000
        }
        
        action = enforcement_client.map_decision_to_action(dgic_response)
        
        assert action["action"] == "fail_safe"


class TestActionExecution:
    """Test suite for action execution"""
    
    def test_allow_execution(self, enforcement_client, sample_dgic_response):
        """Test allow action execution"""
        sample_dgic_response["decision"] = "PROCEED"
        action = enforcement_client.map_decision_to_action(sample_dgic_response)
        result = enforcement_client.execute_action(action)
        
        assert result["status"] == "ALLOWED"
        assert result["action"] == "allow"
        assert "execution_id" in result
    
    def test_escalate_execution(self, enforcement_client, sample_dgic_response):
        """Test escalate action execution"""
        sample_dgic_response["decision"] = "ESCALATE"
        action = enforcement_client.map_decision_to_action(sample_dgic_response)
        result = enforcement_client.execute_action(action)
        
        assert result["status"] == "ESCALATED"
        assert result["action"] == "escalate"
    
    def test_delay_execution(self, enforcement_client, sample_dgic_response):
        """Test delay action execution"""
        sample_dgic_response["decision"] = "HOLD"
        action = enforcement_client.map_decision_to_action(sample_dgic_response)
        result = enforcement_client.execute_action(action)
        
        assert result["status"] == "DELAYED"
        assert result["action"] == "delay"
    
    def test_request_input_execution(self, enforcement_client, sample_dgic_response):
        """Test request_input action execution"""
        sample_dgic_response["decision"] = "REQUEST_MORE_DATA"
        action = enforcement_client.map_decision_to_action(sample_dgic_response)
        result = enforcement_client.execute_action(action)
        
        assert result["status"] == "INPUT_REQUESTED"
        assert result["action"] == "request_input"
    
    def test_fail_safe_execution(self, enforcement_client, sample_dgic_response):
        """Test fail_safe action execution"""
        sample_dgic_response["decision"] = "ERROR"
        action = enforcement_client.map_decision_to_action(sample_dgic_response)
        result = enforcement_client.execute_action(action)
        
        assert result["status"] == "BLOCKED"
        assert result["action"] == "fail_safe"


class TestOverrideMechanism:
    """Test suite for override mechanism"""
    
    def test_override_enabled(self):
        """Test override can be applied when enabled"""
        client = EnforcementDGICClient(enable_override=True)
        dgic_response = {
            "execution_id": "test-override-001",
            "decision": "HOLD",
            "confidence": 0.65,
            "epistemic_state": "AMBIGUOUS",
            "timestamp": 1704067200000
        }
        
        action = client.map_decision_to_action(dgic_response)
        result = client.execute_action(action, override="allow")
        
        assert result["action"] == "allow"
        assert result["override_applied"] is True
        assert result["status"] == "ALLOWED"
    
    def test_override_disabled(self):
        """Test override is ignored when disabled"""
        client = EnforcementDGICClient(enable_override=False)
        dgic_response = {
            "execution_id": "test-override-002",
            "decision": "HOLD",
            "confidence": 0.65,
            "epistemic_state": "AMBIGUOUS",
            "timestamp": 1704067200000
        }
        
        action = client.map_decision_to_action(dgic_response)
        result = client.execute_action(action, override="allow")
        
        assert result["action"] == "delay"  # Original action preserved
        assert result["override_applied"] is False
    
    def test_invalid_override_rejected(self, enforcement_client):
        """Test invalid override action is rejected"""
        dgic_response = {
            "execution_id": "test-override-003",
            "decision": "PROCEED",
            "confidence": 0.9,
            "epistemic_state": "CERTAIN",
            "timestamp": 1704067200000
        }
        
        action = enforcement_client.map_decision_to_action(dgic_response)
        
        with pytest.raises(ValueError, match="Invalid override action"):
            enforcement_client.execute_action(action, override="invalid_action")
    
    def test_override_logged(self):
        """Test override is logged correctly"""
        client = EnforcementDGICClient(enable_override=True)
        dgic_response = {
            "execution_id": "test-override-004",
            "decision": "HOLD",
            "confidence": 0.65,
            "epistemic_state": "AMBIGUOUS",
            "timestamp": 1704067200000
        }
        
        action = client.map_decision_to_action(dgic_response)
        client.execute_action(action, override="escalate")
        
        logs = client.get_action_log()
        override_logs = [log for log in logs if log.get("type") == "OVERRIDE"]
        
        assert len(override_logs) == 1
        assert override_logs[0]["original_action"] == "delay"
        assert override_logs[0]["override_action"] == "escalate"


class TestLoggingAndTracking:
    """Test suite for logging and tracking"""
    
    def test_action_mapping_logged(self, enforcement_client, sample_dgic_response):
        """Test action mapping is logged"""
        enforcement_client.map_decision_to_action(sample_dgic_response)
        
        logs = enforcement_client.get_action_log()
        mapping_logs = [log for log in logs if log.get("type") == "ACTION_MAPPING"]
        
        assert len(mapping_logs) >= 1
        assert mapping_logs[-1]["execution_id"] == sample_dgic_response["execution_id"]
    
    def test_execution_logged(self, enforcement_client, sample_dgic_response):
        """Test action execution is logged"""
        action = enforcement_client.map_decision_to_action(sample_dgic_response)
        enforcement_client.execute_action(action)
        
        logs = enforcement_client.get_action_log()
        execution_logs = [log for log in logs if log.get("type") == "EXECUTION"]
        
        assert len(execution_logs) >= 1
        assert execution_logs[-1]["execution_id"] == sample_dgic_response["execution_id"]
    
    def test_get_log_by_execution_id(self, enforcement_client):
        """Test retrieving logs by execution_id"""
        dgic_response_1 = {
            "execution_id": "test-log-001",
            "decision": "PROCEED",
            "confidence": 0.9,
            "epistemic_state": "CERTAIN",
            "timestamp": 1704067200000
        }
        
        dgic_response_2 = {
            "execution_id": "test-log-002",
            "decision": "ESCALATE",
            "confidence": 0.95,
            "epistemic_state": "CERTAIN",
            "timestamp": 1704067200100
        }
        
        action_1 = enforcement_client.map_decision_to_action(dgic_response_1)
        enforcement_client.execute_action(action_1)
        
        action_2 = enforcement_client.map_decision_to_action(dgic_response_2)
        enforcement_client.execute_action(action_2)
        
        logs_for_001 = enforcement_client.get_action_log(execution_id="test-log-001")
        
        assert len(logs_for_001) >= 2  # At least mapping + execution
        assert all(log["execution_id"] == "test-log-001" for log in logs_for_001)
    
    def test_execution_id_preserved(self, enforcement_client, sample_dgic_response):
        """Test execution_id is preserved through entire flow"""
        execution_id = sample_dgic_response["execution_id"]
        
        action = enforcement_client.map_decision_to_action(sample_dgic_response)
        result = enforcement_client.execute_action(action)
        
        assert action["execution_id"] == execution_id
        assert result["execution_id"] == execution_id


class TestContractCompliance:
    """Test suite for integration contract compliance"""
    
    def test_all_decision_types_supported(self, enforcement_client):
        """Test all contract decision types are supported"""
        valid_decisions = ["PROCEED", "ESCALATE", "HOLD", "REQUEST_MORE_DATA", "ERROR"]
        
        for decision in valid_decisions:
            dgic_response = {
                "execution_id": f"test-{decision}",
                "decision": decision,
                "confidence": 0.5,
                "epistemic_state": "AMBIGUOUS",
                "timestamp": 1704067200000
            }
            
            action = enforcement_client.map_decision_to_action(dgic_response)
            assert action["action"] in ["allow", "escalate", "delay", "request_input", "fail_safe"]
    
    def test_action_result_structure(self, enforcement_client, sample_dgic_response):
        """Test action result has required fields"""
        action = enforcement_client.map_decision_to_action(sample_dgic_response)
        
        required_fields = ["execution_id", "action", "decision", "confidence", "epistemic_state", "timestamp", "source"]
        
        for field in required_fields:
            assert field in action
    
    def test_execution_result_structure(self, enforcement_client, sample_dgic_response):
        """Test execution result has required fields"""
        action = enforcement_client.map_decision_to_action(sample_dgic_response)
        result = enforcement_client.execute_action(action)
        
        required_fields = ["execution_id", "action", "status", "message", "timestamp", "override_applied"]
        
        for field in required_fields:
            assert field in result


class TestConvenienceFunction:
    """Test suite for convenience function"""
    
    def test_consume_dgic_decision(self):
        """Test convenience function works correctly"""
        dgic_response = {
            "execution_id": "test-convenience-001",
            "decision": "PROCEED",
            "confidence": 0.9,
            "epistemic_state": "CERTAIN",
            "timestamp": 1704067200000
        }
        
        result = consume_dgic_decision(dgic_response)
        
        assert result["action"] == "allow"
        assert result["status"] == "ALLOWED"
    
    def test_consume_with_override(self):
        """Test convenience function with override"""
        dgic_response = {
            "execution_id": "test-convenience-002",
            "decision": "HOLD",
            "confidence": 0.65,
            "epistemic_state": "AMBIGUOUS",
            "timestamp": 1704067200000
        }
        
        result = consume_dgic_decision(dgic_response, override="allow")
        
        assert result["action"] == "allow"
        assert result["override_applied"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
