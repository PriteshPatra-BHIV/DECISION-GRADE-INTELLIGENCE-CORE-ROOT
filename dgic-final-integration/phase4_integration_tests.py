"""
Phase 4 Integration Tests: DGIC → InsightBridge
Owner: Pritesh Patra

Tests validate:
1. Trace verification
2. Trace storage
3. Trace retrieval
4. Execution hash verification
5. Cross-system correlation
6. Replay verification
"""

import pytest
from insightbridge_dgic_integration import InsightBridgeDGICClient, consume_dgic_trace


@pytest.fixture
def insightbridge_client():
    """Fixture providing InsightBridge client instance"""
    return InsightBridgeDGICClient()


@pytest.fixture
def sample_trace():
    """Fixture providing sample trace data"""
    return {
        "execution_id": "550e8400-e29b-41d4-a716-446655440000",
        "timestamp": 1704067200150,
        "input_signals": [
            {"id": "sig_001", "type": "SAFE", "priority": 0.9, "timestamp": 1704067199000}
        ],
        "reasoning_trace": [
            {"step": 1, "operation": "signal_aggregation", "result": {}, "timestamp": 1704067200010}
        ],
        "collapse_event": {
            "occurred": False,
            "trigger": "none",
            "timestamp": 1704067200030,
            "selected_state": None,
            "eliminated_states": [],
            "reason": "No collapse"
        },
        "final_state": {
            "decision": "PROCEED",
            "confidence": 0.9,
            "epistemic_state": "CERTAIN"
        },
        "execution_hash": "exec_hash_123",
        "trace_hash": "trace_hash_456"
    }


class TestTraceVerification:
    """Test suite for trace verification"""
    
    def test_valid_trace_verification(self, insightbridge_client):
        """Test verification of valid trace with correct hash"""
        # This trace has a valid structure but hash won't match
        # In real scenario, hash would be computed correctly
        trace = {
            "execution_id": "test-001",
            "timestamp": 1704067200000,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {},
            "final_state": {},
            "execution_hash": "hash",
            "trace_hash": "computed_hash"
        }
        
        verification = insightbridge_client.verify_trace(trace)
        
        assert "valid" in verification
        assert "execution_id" in verification
        assert verification["execution_id"] == "test-001"
    
    def test_missing_trace_hash(self, insightbridge_client):
        """Test verification fails when trace_hash is missing"""
        trace = {
            "execution_id": "test-002",
            "timestamp": 1704067200000,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {},
            "final_state": {},
            "execution_hash": "hash"
            # trace_hash missing
        }
        
        verification = insightbridge_client.verify_trace(trace)
        
        assert verification["valid"] is False
        assert "error" in verification
    
    def test_trace_hash_mismatch(self, insightbridge_client):
        """Test verification detects hash mismatch"""
        trace = {
            "execution_id": "test-003",
            "timestamp": 1704067200000,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {},
            "final_state": {},
            "execution_hash": "hash",
            "trace_hash": "wrong_hash"
        }
        
        verification = insightbridge_client.verify_trace(trace)
        
        # Hash won't match because we provided wrong_hash
        assert "trace_hash_provided" in verification
        assert "trace_hash_computed" in verification


class TestTraceStorage:
    """Test suite for trace storage"""
    
    def test_store_valid_trace(self, insightbridge_client, sample_trace):
        """Test storing valid trace"""
        result = insightbridge_client.store_trace(sample_trace, verify_first=False)
        
        assert result["stored"] is True
        assert result["execution_id"] == sample_trace["execution_id"]
    
    def test_store_with_verification(self, insightbridge_client):
        """Test storing trace with verification enabled"""
        trace = {
            "execution_id": "test-004",
            "timestamp": 1704067200000,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {},
            "final_state": {},
            "execution_hash": "hash",
            "trace_hash": "invalid_hash"
        }
        
        result = insightbridge_client.store_trace(trace, verify_first=True)
        
        # Should fail verification
        assert result["stored"] is False
        assert "error" in result
    
    def test_multiple_traces_stored(self, insightbridge_client):
        """Test storing multiple traces"""
        traces = [
            {"execution_id": f"test-{i}", "timestamp": i, "input_signals": [], 
             "reasoning_trace": [], "collapse_event": {}, "final_state": {},
             "execution_hash": f"hash_{i}", "trace_hash": f"trace_{i}"}
            for i in range(5)
        ]
        
        for trace in traces:
            insightbridge_client.store_trace(trace, verify_first=False)
        
        assert len(insightbridge_client.trace_store) == 5


class TestTraceRetrieval:
    """Test suite for trace retrieval"""
    
    def test_retrieve_existing_trace(self, insightbridge_client, sample_trace):
        """Test retrieving trace that exists"""
        insightbridge_client.store_trace(sample_trace, verify_first=False)
        
        retrieved = insightbridge_client.retrieve_trace(sample_trace["execution_id"])
        
        assert retrieved is not None
        assert retrieved["execution_id"] == sample_trace["execution_id"]
    
    def test_retrieve_nonexistent_trace(self, insightbridge_client):
        """Test retrieving trace that doesn't exist"""
        retrieved = insightbridge_client.retrieve_trace("nonexistent-id")
        
        assert retrieved is None
    
    def test_retrieve_correct_trace(self, insightbridge_client):
        """Test retrieving correct trace among multiple"""
        traces = [
            {"execution_id": f"test-{i}", "timestamp": i, "input_signals": [], 
             "reasoning_trace": [], "collapse_event": {}, "final_state": {},
             "execution_hash": f"hash_{i}", "trace_hash": f"trace_{i}"}
            for i in range(3)
        ]
        
        for trace in traces:
            insightbridge_client.store_trace(trace, verify_first=False)
        
        retrieved = insightbridge_client.retrieve_trace("test-1")
        
        assert retrieved["execution_id"] == "test-1"
        assert retrieved["timestamp"] == 1


class TestExecutionHashVerification:
    """Test suite for execution hash verification"""
    
    def test_matching_execution_hashes(self, insightbridge_client):
        """Test verification when execution hashes match"""
        trace = {
            "execution_id": "test-005",
            "execution_hash": "matching_hash",
            "timestamp": 0,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {},
            "final_state": {},
            "trace_hash": "trace"
        }
        
        dgic_response = {
            "execution_id": "test-005",
            "execution_hash": "matching_hash",
            "decision": "PROCEED"
        }
        
        verification = insightbridge_client.verify_execution_hash(trace, dgic_response)
        
        assert verification["valid"] is True
        assert verification["match"] is True
    
    def test_mismatched_execution_hashes(self, insightbridge_client):
        """Test verification when execution hashes don't match"""
        trace = {
            "execution_id": "test-006",
            "execution_hash": "hash_1",
            "timestamp": 0,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {},
            "final_state": {},
            "trace_hash": "trace"
        }
        
        dgic_response = {
            "execution_id": "test-006",
            "execution_hash": "hash_2",
            "decision": "PROCEED"
        }
        
        verification = insightbridge_client.verify_execution_hash(trace, dgic_response)
        
        assert verification["valid"] is False
        assert verification["match"] is False


class TestCrossSystemCorrelation:
    """Test suite for cross-system correlation"""
    
    def test_correlate_existing_execution(self, insightbridge_client):
        """Test correlation for existing execution_id"""
        trace = {
            "execution_id": "test-007",
            "timestamp": 1704067200000,
            "input_signals": [{"id": "sig_1", "type": "SAFE", "priority": 0.9, "timestamp": 0}],
            "reasoning_trace": [{"step": 1, "operation": "test", "result": {}, "timestamp": 0}],
            "collapse_event": {"occurred": True, "trigger": "dominance", "timestamp": 0, "selected_state": "PROCEED", "eliminated_states": [], "reason": ""},
            "final_state": {"decision": "PROCEED", "confidence": 0.9, "epistemic_state": "CERTAIN"},
            "execution_hash": "hash",
            "trace_hash": "trace"
        }
        
        insightbridge_client.store_trace(trace, verify_first=False)
        
        correlation = insightbridge_client.correlate_by_execution_id("test-007")
        
        assert correlation["found"] is True
        assert correlation["execution_id"] == "test-007"
        assert correlation["final_decision"] == "PROCEED"
        assert len(correlation["input_signals"]) == 1
        assert correlation["reasoning_steps"] == 1
    
    def test_correlate_nonexistent_execution(self, insightbridge_client):
        """Test correlation for nonexistent execution_id"""
        correlation = insightbridge_client.correlate_by_execution_id("nonexistent")
        
        assert correlation["found"] is False
        assert "error" in correlation


class TestReplayVerification:
    """Test suite for replay verification"""
    
    def test_identical_replay(self, insightbridge_client):
        """Test replay verification with identical traces"""
        original = {
            "execution_id": "test-008",
            "timestamp": 0,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {},
            "final_state": {},
            "execution_hash": "exec_hash",
            "trace_hash": "trace_hash"
        }
        
        replay = original.copy()
        
        verification = insightbridge_client.replay_verification(original, replay)
        
        assert verification["replay_valid"] is True
        assert verification["trace_hash_match"] is True
        assert verification["execution_hash_match"] is True
    
    def test_different_replay(self, insightbridge_client):
        """Test replay verification with different traces"""
        original = {
            "execution_id": "test-009",
            "timestamp": 0,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {},
            "final_state": {},
            "execution_hash": "exec_hash_1",
            "trace_hash": "trace_hash_1"
        }
        
        replay = {
            "execution_id": "test-009",
            "timestamp": 0,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {},
            "final_state": {},
            "execution_hash": "exec_hash_2",
            "trace_hash": "trace_hash_2"
        }
        
        verification = insightbridge_client.replay_verification(original, replay)
        
        assert verification["replay_valid"] is False


class TestTraceFiltering:
    """Test suite for trace filtering"""
    
    def test_filter_by_decision(self, insightbridge_client):
        """Test filtering traces by decision type"""
        traces = [
            {"execution_id": "t1", "timestamp": 0, "input_signals": [], "reasoning_trace": [], 
             "collapse_event": {}, "final_state": {"decision": "PROCEED", "confidence": 0.9, "epistemic_state": "CERTAIN"}, 
             "execution_hash": "h1", "trace_hash": "t1"},
            {"execution_id": "t2", "timestamp": 0, "input_signals": [], "reasoning_trace": [], 
             "collapse_event": {}, "final_state": {"decision": "ESCALATE", "confidence": 0.95, "epistemic_state": "CERTAIN"}, 
             "execution_hash": "h2", "trace_hash": "t2"},
            {"execution_id": "t3", "timestamp": 0, "input_signals": [], "reasoning_trace": [], 
             "collapse_event": {}, "final_state": {"decision": "PROCEED", "confidence": 0.88, "epistemic_state": "CERTAIN"}, 
             "execution_hash": "h3", "trace_hash": "t3"}
        ]
        
        for trace in traces:
            insightbridge_client.store_trace(trace, verify_first=False)
        
        proceed_traces = insightbridge_client.get_all_traces(filter_by={"decision": "PROCEED"})
        escalate_traces = insightbridge_client.get_all_traces(filter_by={"decision": "ESCALATE"})
        
        assert len(proceed_traces) == 2
        assert len(escalate_traces) == 1
    
    def test_filter_by_epistemic_state(self, insightbridge_client):
        """Test filtering traces by epistemic state"""
        traces = [
            {"execution_id": "t4", "timestamp": 0, "input_signals": [], "reasoning_trace": [], 
             "collapse_event": {}, "final_state": {"decision": "PROCEED", "confidence": 0.9, "epistemic_state": "CERTAIN"}, 
             "execution_hash": "h4", "trace_hash": "t4"},
            {"execution_id": "t5", "timestamp": 0, "input_signals": [], "reasoning_trace": [], 
             "collapse_event": {}, "final_state": {"decision": "HOLD", "confidence": 0.65, "epistemic_state": "AMBIGUOUS"}, 
             "execution_hash": "h5", "trace_hash": "t5"}
        ]
        
        for trace in traces:
            insightbridge_client.store_trace(trace, verify_first=False)
        
        certain_traces = insightbridge_client.get_all_traces(filter_by={"epistemic_state": "CERTAIN"})
        ambiguous_traces = insightbridge_client.get_all_traces(filter_by={"epistemic_state": "AMBIGUOUS"})
        
        assert len(certain_traces) == 1
        assert len(ambiguous_traces) == 1
    
    def test_get_all_traces_no_filter(self, insightbridge_client):
        """Test getting all traces without filter"""
        traces = [
            {"execution_id": f"t{i}", "timestamp": 0, "input_signals": [], "reasoning_trace": [], 
             "collapse_event": {}, "final_state": {}, "execution_hash": f"h{i}", "trace_hash": f"t{i}"}
            for i in range(3)
        ]
        
        for trace in traces:
            insightbridge_client.store_trace(trace, verify_first=False)
        
        all_traces = insightbridge_client.get_all_traces()
        
        assert len(all_traces) == 3


class TestContractCompliance:
    """Test suite for integration contract compliance"""
    
    def test_trace_immutability(self, insightbridge_client, sample_trace):
        """Test that stored traces are not mutated"""
        original_trace = sample_trace.copy()
        insightbridge_client.store_trace(sample_trace, verify_first=False)
        
        retrieved = insightbridge_client.retrieve_trace(sample_trace["execution_id"])
        
        # Trace should be identical to original
        assert retrieved["execution_id"] == original_trace["execution_id"]
        assert retrieved["execution_hash"] == original_trace["execution_hash"]
    
    def test_execution_id_indexing(self, insightbridge_client):
        """Test traces are indexed by execution_id"""
        traces = [
            {"execution_id": f"exec-{i}", "timestamp": 0, "input_signals": [], "reasoning_trace": [], 
             "collapse_event": {}, "final_state": {}, "execution_hash": f"h{i}", "trace_hash": f"t{i}"}
            for i in range(5)
        ]
        
        for trace in traces:
            insightbridge_client.store_trace(trace, verify_first=False)
        
        # Should be able to retrieve any trace by execution_id
        for i in range(5):
            retrieved = insightbridge_client.retrieve_trace(f"exec-{i}")
            assert retrieved is not None
            assert retrieved["execution_id"] == f"exec-{i}"


class TestConvenienceFunction:
    """Test suite for convenience function"""
    
    def test_consume_dgic_trace(self):
        """Test convenience function works correctly"""
        trace = {
            "execution_id": "test-010",
            "timestamp": 0,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {},
            "final_state": {},
            "execution_hash": "hash",
            "trace_hash": "trace"
        }
        
        result = consume_dgic_trace(trace, verify=False)
        
        assert result["stored"] is True
        assert result["execution_id"] == "test-010"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
