"""
Phase 5 Integration Tests: End-to-End Pipeline
Owner: Pritesh Patra

Tests validate:
1. Complete pipeline execution
2. Cross-system integration
3. Execution ID propagation
4. Data consistency across systems
5. Pipeline error handling
"""

import pytest
import uuid
from end_to_end_pipeline import BHIVPipeline, execute_bhiv_pipeline


@pytest.fixture
def pipeline():
    """Fixture providing BHIV pipeline instance"""
    return BHIVPipeline(dgic_url="http://localhost:8000")


@pytest.fixture
def safe_signals(pipeline):
    """Fixture providing safe signals"""
    return [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
        pipeline.orchestrator.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
    ]


@pytest.fixture
def threat_signals(pipeline):
    """Fixture providing threat signals"""
    return [
        pipeline.orchestrator.create_signal("sig_threat_001", "THREAT", 0.95, "security_agent"),
        pipeline.orchestrator.create_signal("sig_threat_002", "THREAT", 0.90, "anomaly_detector")
    ]


class TestCompletePipeline:
    """Test suite for complete pipeline execution"""
    
    def test_pipeline_executes_successfully(self, pipeline, safe_signals):
        """Test complete pipeline executes without errors"""
        result = pipeline.execute_pipeline(safe_signals)
        
        assert result["success"] is True
        assert "execution_id" in result
        assert "orchestrator" in result
        assert "dgic" in result
        assert "enforcement" in result
        assert "insightbridge" in result
    
    def test_pipeline_with_custom_execution_id(self, pipeline, safe_signals):
        """Test pipeline with custom execution_id"""
        custom_id = str(uuid.uuid4())
        
        result = pipeline.execute_pipeline(safe_signals, execution_id=custom_id)
        
        assert result["execution_id"] == custom_id
    
    def test_pipeline_duration_measured(self, pipeline, safe_signals):
        """Test pipeline duration is measured"""
        result = pipeline.execute_pipeline(safe_signals)
        
        assert "pipeline_duration_ms" in result
        assert result["pipeline_duration_ms"] > 0


class TestOrchestratorIntegration:
    """Test suite for Orchestrator integration in pipeline"""
    
    def test_orchestrator_sends_signals(self, pipeline, safe_signals):
        """Test Orchestrator sends signals to DGIC"""
        result = pipeline.execute_pipeline(safe_signals)
        
        assert result["orchestrator"]["signals_sent"] == len(safe_signals)
        assert "dgic_response" in result["orchestrator"]
    
    def test_orchestrator_receives_dgic_response(self, pipeline, safe_signals):
        """Test Orchestrator receives DGIC response"""
        result = pipeline.execute_pipeline(safe_signals)
        
        dgic_response = result["orchestrator"]["dgic_response"]
        
        assert "decision" in dgic_response
        assert "confidence" in dgic_response
        assert "execution_hash" in dgic_response


class TestDGICIntegration:
    """Test suite for DGIC integration in pipeline"""
    
    def test_dgic_processes_signals(self, pipeline, safe_signals):
        """Test DGIC processes signals and returns decision"""
        result = pipeline.execute_pipeline(safe_signals)
        
        assert "decision" in result["dgic"]
        assert "confidence" in result["dgic"]
        assert "epistemic_state" in result["dgic"]
        assert "execution_hash" in result["dgic"]
    
    def test_dgic_decision_types(self, pipeline):
        """Test DGIC returns valid decision types"""
        valid_decisions = {"PROCEED", "ESCALATE", "HOLD", "REQUEST_MORE_DATA", "ERROR"}
        
        signals = [
            pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent")
        ]
        
        result = pipeline.execute_pipeline(signals)
        
        assert result["dgic"]["decision"] in valid_decisions


class TestEnforcementIntegration:
    """Test suite for Enforcement integration in pipeline"""
    
    def test_enforcement_maps_decision(self, pipeline, safe_signals):
        """Test Enforcement maps DGIC decision to action"""
        result = pipeline.execute_pipeline(safe_signals)
        
        assert "action" in result["enforcement"]
        assert "status" in result["enforcement"]
    
    def test_enforcement_executes_action(self, pipeline, safe_signals):
        """Test Enforcement executes action"""
        result = pipeline.execute_pipeline(safe_signals)
        
        valid_statuses = {"ALLOWED", "ESCALATED", "DELAYED", "INPUT_REQUESTED", "BLOCKED"}
        
        assert result["enforcement"]["status"] in valid_statuses
    
    def test_enforcement_override(self, pipeline, safe_signals):
        """Test Enforcement override mechanism"""
        result = pipeline.execute_pipeline(
            safe_signals,
            enforcement_override="escalate"
        )
        
        assert result["enforcement"]["override_applied"] is True
        assert result["enforcement"]["action"] == "escalate"


class TestInsightBridgeIntegration:
    """Test suite for InsightBridge integration in pipeline"""
    
    def test_insightbridge_stores_trace(self, pipeline, safe_signals):
        """Test InsightBridge stores trace"""
        result = pipeline.execute_pipeline(safe_signals)
        
        assert "trace_stored" in result["insightbridge"]
        assert "trace_hash" in result["insightbridge"]
    
    def test_insightbridge_correlation(self, pipeline, safe_signals):
        """Test InsightBridge correlation"""
        result = pipeline.execute_pipeline(safe_signals)
        
        assert "correlation_found" in result["insightbridge"]


class TestExecutionIDPropagation:
    """Test suite for execution_id propagation across systems"""
    
    def test_execution_id_in_all_systems(self, pipeline, safe_signals):
        """Test execution_id is present in all system responses"""
        result = pipeline.execute_pipeline(safe_signals)
        
        execution_id = result["execution_id"]
        
        # Check Orchestrator
        assert result["orchestrator"]["dgic_response"]["execution_id"] == execution_id
        
        # Check DGIC (implicitly through orchestrator response)
        assert result["orchestrator"]["dgic_response"]["execution_id"] == execution_id
    
    def test_execution_id_preserved_in_trace(self, pipeline, safe_signals):
        """Test execution_id is preserved in InsightBridge trace"""
        result = pipeline.execute_pipeline(safe_signals)
        
        execution_id = result["execution_id"]
        
        # Retrieve trace from InsightBridge
        trace = pipeline.insightbridge.retrieve_trace(execution_id)
        
        assert trace is not None
        assert trace["execution_id"] == execution_id


class TestCrossSystemConsistency:
    """Test suite for data consistency across systems"""
    
    def test_execution_hash_consistency(self, pipeline, safe_signals):
        """Test execution_hash is consistent across systems"""
        result = pipeline.execute_pipeline(safe_signals)
        
        execution_id = result["execution_id"]
        
        # Get execution_hash from DGIC response
        dgic_exec_hash = result["dgic"]["execution_hash"]
        
        # Get execution_hash from InsightBridge trace
        trace = pipeline.insightbridge.retrieve_trace(execution_id)
        trace_exec_hash = trace["execution_hash"]
        
        assert dgic_exec_hash == trace_exec_hash
    
    def test_decision_consistency(self, pipeline, safe_signals):
        """Test decision is consistent across systems"""
        result = pipeline.execute_pipeline(safe_signals)
        
        execution_id = result["execution_id"]
        
        # Get decision from DGIC
        dgic_decision = result["dgic"]["decision"]
        
        # Get decision from InsightBridge trace
        trace = pipeline.insightbridge.retrieve_trace(execution_id)
        trace_decision = trace["final_state"]["decision"]
        
        assert dgic_decision == trace_decision


class TestPipelineScenarios:
    """Test suite for different pipeline scenarios"""
    
    def test_safe_scenario_pipeline(self, pipeline, safe_signals):
        """Test pipeline with safe signals"""
        result = pipeline.execute_pipeline(safe_signals)
        
        assert result["success"] is True
        assert result["dgic"]["decision"] == "PROCEED"
        assert result["enforcement"]["action"] == "allow"
        assert result["enforcement"]["status"] == "ALLOWED"
    
    def test_threat_scenario_pipeline(self, pipeline, threat_signals):
        """Test pipeline with threat signals"""
        result = pipeline.execute_pipeline(threat_signals)
        
        assert result["success"] is True
        assert result["dgic"]["decision"] == "ESCALATE"
        assert result["enforcement"]["action"] == "escalate"
        assert result["enforcement"]["status"] == "ESCALATED"
    
    def test_ambiguous_scenario_pipeline(self, pipeline):
        """Test pipeline with ambiguous signals"""
        signals = [
            pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.6, "agent_alpha"),
            pipeline.orchestrator.create_signal("sig_002", "UNKNOWN", 0.5, "agent_beta")
        ]
        
        result = pipeline.execute_pipeline(signals)
        
        assert result["success"] is True
        assert result["dgic"]["decision"] == "HOLD"
        assert result["enforcement"]["action"] == "delay"
        assert result["enforcement"]["status"] == "DELAYED"


class TestPipelineLogging:
    """Test suite for pipeline logging"""
    
    def test_execution_logged(self, pipeline, safe_signals):
        """Test pipeline execution is logged"""
        initial_log_count = len(pipeline.get_execution_log())
        
        pipeline.execute_pipeline(safe_signals)
        
        final_log_count = len(pipeline.get_execution_log())
        
        assert final_log_count == initial_log_count + 1
    
    def test_multiple_executions_logged(self, pipeline, safe_signals):
        """Test multiple executions are logged"""
        for _ in range(3):
            pipeline.execute_pipeline(safe_signals)
        
        log = pipeline.get_execution_log()
        
        assert len(log) == 3
    
    def test_execution_summary_retrieval(self, pipeline, safe_signals):
        """Test execution summary can be retrieved"""
        result = pipeline.execute_pipeline(safe_signals)
        execution_id = result["execution_id"]
        
        summary = pipeline.get_execution_summary(execution_id)
        
        assert summary["execution_id"] == execution_id
        assert "dgic" in summary
        assert "enforcement" in summary


class TestConvenienceFunction:
    """Test suite for convenience function"""
    
    def test_execute_bhiv_pipeline(self):
        """Test convenience function works"""
        pipeline = BHIVPipeline(dgic_url="http://localhost:8000")
        signals = [
            pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent")
        ]
        
        result = execute_bhiv_pipeline(signals)
        
        assert result["success"] is True
        assert "execution_id" in result


class TestPipelineIntegrity:
    """Test suite for pipeline integrity"""
    
    def test_pipeline_maintains_immutability(self, pipeline, safe_signals):
        """Test pipeline doesn't mutate data"""
        original_signals = [s.copy() for s in safe_signals]
        
        pipeline.execute_pipeline(safe_signals)
        
        # Signals should not be mutated
        for i, sig in enumerate(safe_signals):
            assert sig["id"] == original_signals[i]["id"]
            assert sig["type"] == original_signals[i]["type"]
            assert sig["priority"] == original_signals[i]["priority"]
    
    def test_pipeline_determinism(self, pipeline, safe_signals):
        """Test pipeline produces consistent results for same input"""
        execution_id = str(uuid.uuid4())
        
        result1 = pipeline.execute_pipeline(safe_signals, execution_id=execution_id)
        result2 = pipeline.execute_pipeline(safe_signals, execution_id=execution_id)
        
        # Execution hashes should match
        assert result1["dgic"]["execution_hash"] == result2["dgic"]["execution_hash"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
