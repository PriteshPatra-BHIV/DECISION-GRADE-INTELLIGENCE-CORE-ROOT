"""
Phase 6 Integration Tests: Failure Flow Integration
Owner: Pritesh Patra

Tests validate:
1. DGIC failure handling
2. Enforcement failure handling
3. InsightBridge failure handling
4. Fail-safe behavior
5. Error logging
6. Chain integrity
"""

import pytest
import uuid
from failure_flow_pipeline import ResilientBHIVPipeline, FailureType


@pytest.fixture
def resilient_pipeline():
    """Fixture providing resilient pipeline instance"""
    return ResilientBHIVPipeline(dgic_url="http://localhost:8000")


@pytest.fixture
def safe_signals(resilient_pipeline):
    """Fixture providing safe signals"""
    return [
        resilient_pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
        resilient_pipeline.orchestrator.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
    ]


class TestDGICFailureHandling:
    """Test suite for DGIC failure handling"""
    
    def test_dgic_unreachable_fails_safe(self, resilient_pipeline, safe_signals):
        """Test DGIC unreachable results in fail-safe"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        assert len(result["failures"]) > 0
        assert result["dgic"]["decision"] == "ERROR"
        assert result["enforcement"]["action"] == "fail_safe"
        assert result["enforcement"]["status"] == "BLOCKED"
    
    def test_dgic_timeout_fails_safe(self, resilient_pipeline, safe_signals):
        """Test DGIC timeout results in fail-safe"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_TIMEOUT
        )
        
        assert len(result["failures"]) > 0
        assert result["dgic"]["decision"] == "ERROR"
        assert result["enforcement"]["status"] == "BLOCKED"
    
    def test_dgic_failure_logged(self, resilient_pipeline, safe_signals):
        """Test DGIC failure is logged correctly"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        assert len(result["failures"]) > 0
        failure = result["failures"][0]
        
        assert "type" in failure
        assert "execution_id" in failure
        assert "timestamp" in failure
        assert failure["handled"] is True


class TestEnforcementFailureHandling:
    """Test suite for Enforcement failure handling"""
    
    def test_enforcement_error_fails_safe(self, resilient_pipeline, safe_signals):
        """Test Enforcement error results in fail-safe"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.ENFORCEMENT_ERROR
        )
        
        assert len(result["failures"]) > 0
        assert result["enforcement"]["action"] == "fail_safe"
        assert result["enforcement"]["status"] == "BLOCKED"
    
    def test_enforcement_failure_logged(self, resilient_pipeline, safe_signals):
        """Test Enforcement failure is logged"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.ENFORCEMENT_ERROR
        )
        
        enforcement_failures = [f for f in result["failures"] if f["type"] == "ENFORCEMENT_ERROR"]
        
        assert len(enforcement_failures) > 0
        assert enforcement_failures[0]["handled"] is True


class TestInsightBridgeFailureHandling:
    """Test suite for InsightBridge failure handling"""
    
    def test_insightbridge_error_continues(self, resilient_pipeline, safe_signals):
        """Test InsightBridge error allows pipeline to continue"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.INSIGHTBRIDGE_ERROR
        )
        
        # InsightBridge failure should not block pipeline
        assert result["dgic"]["decision"] == "PROCEED"
        assert result["enforcement"]["status"] == "ALLOWED"
        assert result["insightbridge"]["trace_stored"] is False
    
    def test_insightbridge_failure_acceptable(self, resilient_pipeline, safe_signals):
        """Test InsightBridge failure is acceptable per contract"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.INSIGHTBRIDGE_ERROR
        )
        
        insightbridge_failures = [f for f in result["failures"] if f["type"] == "INSIGHTBRIDGE_ERROR"]
        
        assert len(insightbridge_failures) > 0
        assert insightbridge_failures[0]["recovery"] == "continue_without_trace"


class TestInvalidInputHandling:
    """Test suite for invalid input handling"""
    
    def test_invalid_signals_rejected(self, resilient_pipeline, safe_signals):
        """Test invalid signals are rejected"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.INVALID_SIGNALS
        )
        
        assert result["success"] is False
        assert "error" in result
        assert result["stage"] == "Input Validation"
    
    def test_invalid_input_logged(self, resilient_pipeline, safe_signals):
        """Test invalid input is logged"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.INVALID_SIGNALS
        )
        
        assert len(result["failures"]) > 0
        assert result["failures"][0]["type"] == "INVALID_INPUT"


class TestFailSafeBehavior:
    """Test suite for fail-safe behavior"""
    
    def test_error_decision_triggers_fail_safe(self, resilient_pipeline, safe_signals):
        """Test ERROR decision triggers fail_safe action"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        assert result["dgic"]["decision"] == "ERROR"
        assert result["enforcement"]["action"] == "fail_safe"
        assert result["enforcement"]["status"] == "BLOCKED"
    
    def test_fail_safe_blocks_operation(self, resilient_pipeline, safe_signals):
        """Test fail_safe blocks operation"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.ENFORCEMENT_ERROR
        )
        
        assert result["enforcement"]["status"] == "BLOCKED"


class TestErrorLogging:
    """Test suite for error logging"""
    
    def test_failures_logged_with_details(self, resilient_pipeline, safe_signals):
        """Test failures are logged with complete details"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        assert len(result["failures"]) > 0
        failure = result["failures"][0]
        
        required_fields = ["type", "execution_id", "error", "timestamp", "handled", "recovery"]
        for field in required_fields:
            assert field in failure
    
    def test_recovery_actions_logged(self, resilient_pipeline, safe_signals):
        """Test recovery actions are logged"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        assert len(result["recovery_actions"]) > 0
    
    def test_failure_log_accumulates(self, resilient_pipeline, safe_signals):
        """Test failure log accumulates across executions"""
        initial_log_count = len(resilient_pipeline.get_failure_log())
        
        resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        final_log_count = len(resilient_pipeline.get_failure_log())
        
        assert final_log_count == initial_log_count + 1


class TestChainIntegrity:
    """Test suite for chain integrity during failures"""
    
    def test_execution_id_preserved_on_failure(self, resilient_pipeline, safe_signals):
        """Test execution_id is preserved even when failures occur"""
        execution_id = str(uuid.uuid4())
        
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            execution_id=execution_id,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        assert result["execution_id"] == execution_id
        assert result["orchestrator"]["dgic_response"]["execution_id"] == execution_id
    
    def test_pipeline_completes_despite_failures(self, resilient_pipeline, safe_signals):
        """Test pipeline completes even with failures"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        # Pipeline should complete with fail-safe
        assert "pipeline_duration_ms" in result
        assert result["pipeline_duration_ms"] > 0
    
    def test_chain_not_broken_by_failure(self, resilient_pipeline, safe_signals):
        """Test failure doesn't break the chain"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.ENFORCEMENT_ERROR
        )
        
        # All stages should have results
        assert "orchestrator" in result
        assert "dgic" in result
        assert "enforcement" in result
        assert "insightbridge" in result


class TestMultipleFailures:
    """Test suite for handling multiple failures"""
    
    def test_multiple_failures_handled_independently(self, resilient_pipeline, safe_signals):
        """Test multiple failures are handled independently"""
        failure_types = [
            FailureType.DGIC_UNREACHABLE,
            FailureType.ENFORCEMENT_ERROR,
            FailureType.INSIGHTBRIDGE_ERROR
        ]
        
        for failure_type in failure_types:
            result = resilient_pipeline.execute_with_failure_handling(
                safe_signals,
                inject_failure=failure_type
            )
            
            assert len(result["failures"]) > 0
            assert all(f["handled"] for f in result["failures"])
    
    def test_failure_log_tracks_all_failures(self, resilient_pipeline, safe_signals):
        """Test failure log tracks all failures across executions"""
        failure_types = [
            FailureType.DGIC_UNREACHABLE,
            FailureType.ENFORCEMENT_ERROR
        ]
        
        for failure_type in failure_types:
            resilient_pipeline.execute_with_failure_handling(
                safe_signals,
                inject_failure=failure_type
            )
        
        failure_log = resilient_pipeline.get_failure_log()
        
        assert len(failure_log) == 2
        assert all(len(log["failures"]) > 0 for log in failure_log)


class TestRecoveryMechanisms:
    """Test suite for recovery mechanisms"""
    
    def test_dgic_failure_recovery_is_fail_safe(self, resilient_pipeline, safe_signals):
        """Test DGIC failure recovery is fail-safe"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        assert result["failures"][0]["recovery"] == "fail_safe"
    
    def test_enforcement_failure_recovery_is_fail_safe(self, resilient_pipeline, safe_signals):
        """Test Enforcement failure recovery is fail-safe"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.ENFORCEMENT_ERROR
        )
        
        enforcement_failure = [f for f in result["failures"] if f["type"] == "ENFORCEMENT_ERROR"][0]
        
        assert enforcement_failure["recovery"] == "fail_safe"
    
    def test_insightbridge_failure_recovery_continues(self, resilient_pipeline, safe_signals):
        """Test InsightBridge failure recovery allows continuation"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.INSIGHTBRIDGE_ERROR
        )
        
        insightbridge_failure = [f for f in result["failures"] if f["type"] == "INSIGHTBRIDGE_ERROR"][0]
        
        assert insightbridge_failure["recovery"] == "continue_without_trace"


class TestFailureMetrics:
    """Test suite for failure metrics"""
    
    def test_failure_count_tracked(self, resilient_pipeline, safe_signals):
        """Test failure count is tracked"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        assert len(result["failures"]) == 1
    
    def test_recovery_action_count_tracked(self, resilient_pipeline, safe_signals):
        """Test recovery action count is tracked"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        assert len(result["recovery_actions"]) == 1
    
    def test_pipeline_duration_measured_with_failures(self, resilient_pipeline, safe_signals):
        """Test pipeline duration is measured even with failures"""
        result = resilient_pipeline.execute_with_failure_handling(
            safe_signals,
            inject_failure=FailureType.DGIC_UNREACHABLE
        )
        
        assert "pipeline_duration_ms" in result
        assert result["pipeline_duration_ms"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
