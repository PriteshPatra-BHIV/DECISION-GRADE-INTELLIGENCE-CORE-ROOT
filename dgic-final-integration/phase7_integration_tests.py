"""
Phase 7: Replay System Integration Tests
Comprehensive tests for replay functionality
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dgic_final_integration.replay_system import ReplaySystem, ReplayStatus, SystemState
from dgic_final_integration.insightbridge_dgic_integration import InsightBridgeDGICClient


class TestReplaySystem(unittest.TestCase):
    """Test suite for ReplaySystem"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_insightbridge = Mock(spec=InsightBridgeDGICClient)
        self.replay_system = ReplaySystem(self.mock_insightbridge)
        
        self.sample_trace = {
            "trace": {
                "execution_id": "550e8400-e29b-41d4-a716-446655440001",
                "signals": [{"type": "risk", "value": 0.8}],
                "decision": "PROCEED",
                "confidence": 0.95,
                "reasoning": "Low risk detected",
                "action_taken": "allow",
                "trace_hash": "abc123",
                "timestamp": "2024-01-15T10:00:00Z"
            },
            "stored_at": "2024-01-15T10:00:01Z"
        }
    
    def test_replay_execution_success(self):
        """Test successful execution replay"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        result = self.replay_system.replay_execution("550e8400-e29b-41d4-a716-446655440001")
        
        self.assertEqual(result["execution_id"], "550e8400-e29b-41d4-a716-446655440001")
        self.assertEqual(result["replay_status"], ReplayStatus.VERIFIED.value)
        self.assertGreater(len(result["timeline"]), 0)
        self.assertIn("orchestrator", result["system_states"])
    
    def test_replay_execution_no_trace(self):
        """Test replay when no trace found"""
        self.mock_insightbridge.retrieve_trace.return_value = None
        
        result = self.replay_system.replay_execution("550e8400-e29b-41d4-a716-446655440001")
        
        self.assertEqual(result["replay_status"], ReplayStatus.INCOMPLETE.value)
        self.assertIn("No trace found", result["errors"][0])
    
    def test_replay_execution_hash_mismatch(self):
        """Test replay with hash verification failure"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        self.mock_insightbridge.verify_execution_hash.return_value = False
        
        result = self.replay_system.replay_execution("550e8400-e29b-41d4-a716-446655440001")
        
        self.assertEqual(result["replay_status"], ReplayStatus.HASH_MISMATCH.value)
        self.assertIn("hash verification failed", result["errors"][0].lower())
    
    def test_replay_batch_success(self):
        """Test batch replay of multiple executions"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        execution_ids = ["exec1", "exec2", "exec3"]
        result = self.replay_system.replay_batch(execution_ids)
        
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["verified"], 3)
        self.assertEqual(result["failed"], 0)
        self.assertEqual(len(result["results"]), 3)
    
    def test_replay_batch_mixed_results(self):
        """Test batch replay with mixed success/failure"""
        def mock_retrieve(exec_id):
            if exec_id == "exec2":
                return None
            return self.sample_trace
        
        self.mock_insightbridge.retrieve_trace.side_effect = mock_retrieve
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        execution_ids = ["exec1", "exec2", "exec3"]
        result = self.replay_system.replay_batch(execution_ids)
        
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["verified"], 2)
        self.assertEqual(result["failed"], 1)
    
    def test_verify_decision_chain_valid(self):
        """Test decision chain verification - valid chain"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        
        result = self.replay_system.verify_decision_chain("550e8400-e29b-41d4-a716-446655440001")
        
        self.assertTrue(result["chain_valid"])
        self.assertTrue(result["signal_to_decision"])
        self.assertTrue(result["decision_to_action"])
        self.assertTrue(result["action_to_trace"])
    
    def test_verify_decision_chain_invalid_mapping(self):
        """Test decision chain verification - invalid decision-action mapping"""
        invalid_trace = self.sample_trace.copy()
        invalid_trace["trace"] = self.sample_trace["trace"].copy()
        invalid_trace["trace"]["decision"] = "PROCEED"
        invalid_trace["trace"]["action_taken"] = "escalate"
        
        self.mock_insightbridge.retrieve_trace.return_value = invalid_trace
        
        result = self.replay_system.verify_decision_chain("550e8400-e29b-41d4-a716-446655440001")
        
        self.assertFalse(result["chain_valid"])
        self.assertFalse(result["decision_to_action"])
        self.assertIn("Invalid decision-action mapping", result["errors"][0])
    
    def test_verify_decision_chain_no_trace(self):
        """Test decision chain verification - no trace found"""
        self.mock_insightbridge.retrieve_trace.return_value = None
        
        result = self.replay_system.verify_decision_chain("550e8400-e29b-41d4-a716-446655440001")
        
        self.assertFalse(result["chain_valid"])
        self.assertIn("No trace found", result["errors"][0])
    
    def test_reconstruct_timeline(self):
        """Test timeline reconstruction"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        result = self.replay_system.replay_execution("550e8400-e29b-41d4-a716-446655440001")
        timeline = result["timeline"]
        
        self.assertEqual(len(timeline), 4)
        self.assertEqual(timeline[0]["system"], SystemState.ORCHESTRATOR.value)
        self.assertEqual(timeline[1]["system"], SystemState.DGIC.value)
        self.assertEqual(timeline[2]["system"], SystemState.ENFORCEMENT.value)
        self.assertEqual(timeline[3]["system"], SystemState.INSIGHTBRIDGE.value)
    
    def test_extract_system_states(self):
        """Test system state extraction"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        result = self.replay_system.replay_execution("550e8400-e29b-41d4-a716-446655440001")
        states = result["system_states"]
        
        self.assertIn(SystemState.ORCHESTRATOR.value, states)
        self.assertIn(SystemState.DGIC.value, states)
        self.assertIn(SystemState.ENFORCEMENT.value, states)
        self.assertIn(SystemState.INSIGHTBRIDGE.value, states)
        
        self.assertEqual(states[SystemState.DGIC.value]["decision"], "PROCEED")
        self.assertEqual(states[SystemState.ENFORCEMENT.value]["action_taken"], "allow")
    
    def test_verify_execution_integrity_valid(self):
        """Test execution integrity verification - valid"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        result = self.replay_system.replay_execution("550e8400-e29b-41d4-a716-446655440001")
        verification = result["verification"]
        
        self.assertTrue(verification["integrity_valid"])
        self.assertTrue(verification["execution_id_present"])
        self.assertTrue(verification["decision_present"])
        self.assertTrue(verification["action_present"])
    
    def test_verify_execution_integrity_incomplete(self):
        """Test execution integrity verification - incomplete trace"""
        incomplete_trace = {
            "trace": {
                "execution_id": "550e8400-e29b-41d4-a716-446655440001",
                "decision": "PROCEED"
            },
            "stored_at": "2024-01-15T10:00:01Z"
        }
        
        self.mock_insightbridge.retrieve_trace.return_value = incomplete_trace
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        result = self.replay_system.replay_execution("550e8400-e29b-41d4-a716-446655440001")
        verification = result["verification"]
        
        self.assertFalse(verification["integrity_valid"])
    
    def test_compare_executions_identical(self):
        """Test execution comparison - identical executions"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        result = self.replay_system.compare_executions("exec1", "exec2")
        
        self.assertTrue(result["status_match"])
        self.assertTrue(result["decision_match"])
        self.assertTrue(result["action_match"])
        self.assertEqual(len(result["differences"]), 0)
    
    def test_compare_executions_different(self):
        """Test execution comparison - different executions"""
        trace1 = self.sample_trace.copy()
        trace2 = {
            "trace": {
                "execution_id": "550e8400-e29b-41d4-a716-446655440002",
                "signals": [{"type": "risk", "value": 0.9}],
                "decision": "ESCALATE",
                "confidence": 0.85,
                "reasoning": "High risk detected",
                "action_taken": "escalate",
                "trace_hash": "def456",
                "timestamp": "2024-01-15T10:05:00Z"
            },
            "stored_at": "2024-01-15T10:05:01Z"
        }
        
        def mock_retrieve(exec_id):
            return trace1 if exec_id == "exec1" else trace2
        
        self.mock_insightbridge.retrieve_trace.side_effect = mock_retrieve
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        result = self.replay_system.compare_executions("exec1", "exec2")
        
        self.assertFalse(result["decision_match"])
        self.assertFalse(result["action_match"])
        self.assertGreater(len(result["differences"]), 0)
    
    def test_audit_trail_generation(self):
        """Test audit trail generation"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        audit = self.replay_system.audit_trail("550e8400-e29b-41d4-a716-446655440001")
        
        self.assertEqual(audit["execution_id"], "550e8400-e29b-41d4-a716-446655440001")
        self.assertIn("audit_timestamp", audit)
        self.assertGreater(len(audit["events"]), 0)
        self.assertIn("summary", audit)
        self.assertEqual(audit["summary"]["total_events"], len(audit["events"]))
    
    def test_validate_decision_action_mapping_proceed(self):
        """Test decision-action mapping validation - PROCEED"""
        valid = self.replay_system._validate_decision_action_mapping("PROCEED", "allow")
        self.assertTrue(valid)
    
    def test_validate_decision_action_mapping_escalate(self):
        """Test decision-action mapping validation - ESCALATE"""
        valid = self.replay_system._validate_decision_action_mapping("ESCALATE", "escalate")
        self.assertTrue(valid)
    
    def test_validate_decision_action_mapping_hold(self):
        """Test decision-action mapping validation - HOLD"""
        valid = self.replay_system._validate_decision_action_mapping("HOLD", "delay")
        self.assertTrue(valid)
    
    def test_validate_decision_action_mapping_request_more_data(self):
        """Test decision-action mapping validation - REQUEST_MORE_DATA"""
        valid = self.replay_system._validate_decision_action_mapping("REQUEST_MORE_DATA", "request_input")
        self.assertTrue(valid)
    
    def test_validate_decision_action_mapping_error(self):
        """Test decision-action mapping validation - ERROR"""
        valid = self.replay_system._validate_decision_action_mapping("ERROR", "fail_safe")
        self.assertTrue(valid)
    
    def test_validate_decision_action_mapping_invalid(self):
        """Test decision-action mapping validation - invalid mapping"""
        valid = self.replay_system._validate_decision_action_mapping("PROCEED", "escalate")
        self.assertFalse(valid)
    
    def test_replay_cache(self):
        """Test replay result caching"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        exec_id = "550e8400-e29b-41d4-a716-446655440001"
        result = self.replay_system.replay_execution(exec_id)
        
        self.assertIn(exec_id, self.replay_system.replay_cache)
        self.assertEqual(self.replay_system.replay_cache[exec_id], result)
    
    def test_replay_execution_exception_handling(self):
        """Test replay execution with exception"""
        self.mock_insightbridge.retrieve_trace.side_effect = Exception("Connection error")
        
        result = self.replay_system.replay_execution("550e8400-e29b-41d4-a716-446655440001")
        
        self.assertEqual(result["replay_status"], ReplayStatus.CORRUPTED.value)
        self.assertIn("Replay failed", result["errors"][0])
    
    def test_timeline_event_structure(self):
        """Test timeline event structure"""
        self.mock_insightbridge.retrieve_trace.return_value = self.sample_trace
        self.mock_insightbridge.verify_execution_hash.return_value = True
        
        result = self.replay_system.replay_execution("550e8400-e29b-41d4-a716-446655440001")
        
        for event in result["timeline"]:
            self.assertIn("timestamp", event)
            self.assertIn("system", event)
            self.assertIn("action", event)
            self.assertIn("details", event)


def run_tests():
    """Run all tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestReplaySystem)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("PHASE 7: REPLAY SYSTEM INTEGRATION TESTS")
    print("=" * 70)
    
    success = run_tests()
    
    print("\n" + "=" * 70)
    if success:
        print("✓ All replay system tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 70)
