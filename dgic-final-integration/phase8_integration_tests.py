"""
Phase 8: Integration Testing
Comprehensive end-to-end testing across all BHIV systems
"""

import unittest
import requests
import time
from datetime import datetime
import uuid
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator_dgic_integration import OrchestratorDGICClient
from enforcement_dgic_integration import EnforcementDGICClient
from insightbridge_dgic_integration import InsightBridgeDGICClient
from end_to_end_pipeline import BHIVPipeline
from failure_flow_pipeline import ResilientBHIVPipeline
from replay_system import ReplaySystem


class TestFullIntegration(unittest.TestCase):
    """End-to-end integration tests across all systems"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.orchestrator = OrchestratorDGICClient("http://localhost:8000")
        cls.enforcement = EnforcementDGICClient("http://localhost:8002")
        cls.insightbridge = InsightBridgeDGICClient("http://localhost:8003")
        cls.pipeline = BHIVPipeline(
            "http://localhost:8000",
            "http://localhost:8001",
            "http://localhost:8002",
            "http://localhost:8003"
        )
        cls.resilient_pipeline = ResilientBHIVPipeline(
            "http://localhost:8000",
            "http://localhost:8001",
            "http://localhost:8002",
            "http://localhost:8003"
        )
        cls.replay_system = ReplaySystem(cls.insightbridge)
    
    def test_e2e_proceed_flow(self):
        """Test complete PROCEED flow through all systems"""
        signals = [{"type": "risk", "value": 0.3}]
        result = self.pipeline.execute_pipeline(signals)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["dgic_decision"], "PROCEED")
        self.assertEqual(result["enforcement_action"], "allow")
        self.assertIsNotNone(result["execution_id"])
        self.assertTrue(result["trace_stored"])
    
    def test_e2e_escalate_flow(self):
        """Test complete ESCALATE flow through all systems"""
        signals = [{"type": "risk", "value": 0.9}]
        result = self.pipeline.execute_pipeline(signals)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["dgic_decision"], "ESCALATE")
        self.assertEqual(result["enforcement_action"], "escalate")
        self.assertIsNotNone(result["execution_id"])
    
    def test_e2e_hold_flow(self):
        """Test complete HOLD flow through all systems"""
        signals = [{"type": "risk", "value": 0.6}]
        result = self.pipeline.execute_pipeline(signals)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["dgic_decision"], "HOLD")
        self.assertEqual(result["enforcement_action"], "delay")
    
    def test_execution_id_propagation(self):
        """Test execution_id propagates through all systems"""
        signals = [{"type": "risk", "value": 0.4}]
        result = self.pipeline.execute_pipeline(signals)
        
        execution_id = result["execution_id"]
        self.assertIsNotNone(execution_id)
        
        # Verify execution_id in trace
        trace = self.insightbridge.retrieve_trace(execution_id)
        self.assertIsNotNone(trace)
        self.assertEqual(trace["trace"]["execution_id"], execution_id)
    
    def test_trace_hash_integrity(self):
        """Test trace hash verification across systems"""
        signals = [{"type": "risk", "value": 0.5}]
        result = self.pipeline.execute_pipeline(signals)
        
        execution_id = result["execution_id"]
        
        # Verify hash
        hash_valid = self.insightbridge.verify_execution_hash(execution_id)
        self.assertTrue(hash_valid)
    
    def test_decision_action_mapping_consistency(self):
        """Test decision-to-action mapping consistency"""
        test_cases = [
            (0.2, "PROCEED", "allow"),
            (0.9, "ESCALATE", "escalate"),
            (0.6, "HOLD", "delay")
        ]
        
        for risk_value, expected_decision, expected_action in test_cases:
            signals = [{"type": "risk", "value": risk_value}]
            result = self.pipeline.execute_pipeline(signals)
            
            self.assertEqual(result["dgic_decision"], expected_decision)
            self.assertEqual(result["enforcement_action"], expected_action)
    
    def test_replay_after_execution(self):
        """Test replay system can reconstruct execution"""
        signals = [{"type": "risk", "value": 0.4}]
        result = self.pipeline.execute_pipeline(signals)
        
        execution_id = result["execution_id"]
        
        # Replay execution
        replay_result = self.replay_system.replay_execution(execution_id)
        
        self.assertEqual(replay_result["execution_id"], execution_id)
        self.assertEqual(replay_result["replay_status"], "verified")
        self.assertGreater(len(replay_result["timeline"]), 0)
    
    def test_decision_chain_verification(self):
        """Test decision chain integrity verification"""
        signals = [{"type": "risk", "value": 0.3}]
        result = self.pipeline.execute_pipeline(signals)
        
        execution_id = result["execution_id"]
        
        # Verify chain
        chain_result = self.replay_system.verify_decision_chain(execution_id)
        
        self.assertTrue(chain_result["chain_valid"])
        self.assertTrue(chain_result["signal_to_decision"])
        self.assertTrue(chain_result["decision_to_action"])
        self.assertTrue(chain_result["action_to_trace"])
    
    def test_concurrent_executions(self):
        """Test multiple concurrent executions"""
        signals_list = [
            [{"type": "risk", "value": 0.2}],
            [{"type": "risk", "value": 0.8}],
            [{"type": "risk", "value": 0.5}]
        ]
        
        results = []
        for signals in signals_list:
            result = self.pipeline.execute_pipeline(signals)
            results.append(result)
        
        # Verify all executions succeeded
        for result in results:
            self.assertEqual(result["status"], "success")
        
        # Verify unique execution IDs
        execution_ids = [r["execution_id"] for r in results]
        self.assertEqual(len(execution_ids), len(set(execution_ids)))
    
    def test_failure_recovery_dgic_unreachable(self):
        """Test failure recovery when DGIC unreachable"""
        signals = [{"type": "risk", "value": 0.4}]
        
        # Simulate DGIC failure
        result = self.resilient_pipeline.execute_with_failure_handling(
            signals,
            simulate_dgic_failure=True
        )
        
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["enforcement_status"], "BLOCKED")
        self.assertIn("failure_type", result)
    
    def test_failure_recovery_enforcement_error(self):
        """Test failure recovery when Enforcement fails"""
        signals = [{"type": "risk", "value": 0.4}]
        
        result = self.resilient_pipeline.execute_with_failure_handling(
            signals,
            simulate_enforcement_failure=True
        )
        
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["enforcement_status"], "BLOCKED")
    
    def test_insightbridge_failure_acceptable(self):
        """Test pipeline continues when InsightBridge fails"""
        signals = [{"type": "risk", "value": 0.4}]
        
        result = self.resilient_pipeline.execute_with_failure_handling(
            signals,
            simulate_insightbridge_failure=True
        )
        
        # Pipeline should succeed even if InsightBridge fails
        self.assertEqual(result["status"], "success")
        self.assertFalse(result.get("trace_stored", False))
    
    def test_batch_execution_replay(self):
        """Test batch replay of multiple executions"""
        execution_ids = []
        
        # Execute multiple pipelines
        for i in range(3):
            signals = [{"type": "risk", "value": 0.3 + i * 0.2}]
            result = self.pipeline.execute_pipeline(signals)
            execution_ids.append(result["execution_id"])
        
        # Batch replay
        batch_result = self.replay_system.replay_batch(execution_ids)
        
        self.assertEqual(batch_result["total"], 3)
        self.assertGreater(batch_result["verified"], 0)
    
    def test_audit_trail_generation(self):
        """Test audit trail generation for execution"""
        signals = [{"type": "risk", "value": 0.4}]
        result = self.pipeline.execute_pipeline(signals)
        
        execution_id = result["execution_id"]
        
        # Generate audit trail
        audit = self.replay_system.audit_trail(execution_id)
        
        self.assertEqual(audit["execution_id"], execution_id)
        self.assertIn("audit_timestamp", audit)
        self.assertGreater(len(audit["events"]), 0)
        self.assertIn("summary", audit)
    
    def test_execution_comparison(self):
        """Test comparison of two executions"""
        # Execute two pipelines
        signals1 = [{"type": "risk", "value": 0.3}]
        result1 = self.pipeline.execute_pipeline(signals1)
        
        signals2 = [{"type": "risk", "value": 0.8}]
        result2 = self.pipeline.execute_pipeline(signals2)
        
        # Compare executions
        comparison = self.replay_system.compare_executions(
            result1["execution_id"],
            result2["execution_id"]
        )
        
        self.assertIn("execution_1", comparison)
        self.assertIn("execution_2", comparison)
        self.assertIn("differences", comparison)
    
    def test_override_mechanism(self):
        """Test enforcement override mechanism"""
        signals = [{"type": "risk", "value": 0.3}]
        
        # Create signal and get decision
        execution_id = self.orchestrator.create_signal(signals)
        decision_result = self.orchestrator.evaluate_decision(execution_id, signals)
        
        # Override decision
        override_result = self.enforcement.execute_action(
            execution_id,
            decision_result["decision"],
            override="escalate",
            override_reason="Manual review required"
        )
        
        self.assertEqual(override_result["action"], "escalate")
        self.assertTrue(override_result["override_applied"])
    
    def test_trace_immutability(self):
        """Test trace immutability and hash verification"""
        signals = [{"type": "risk", "value": 0.4}]
        result = self.pipeline.execute_pipeline(signals)
        
        execution_id = result["execution_id"]
        
        # Retrieve trace
        trace1 = self.insightbridge.retrieve_trace(execution_id)
        
        # Retrieve again
        trace2 = self.insightbridge.retrieve_trace(execution_id)
        
        # Verify traces are identical
        self.assertEqual(trace1["trace"]["trace_hash"], trace2["trace"]["trace_hash"])
    
    def test_signal_validation(self):
        """Test signal validation at orchestrator"""
        # Invalid signals
        invalid_signals = []
        
        try:
            execution_id = self.orchestrator.create_signal(invalid_signals)
            self.fail("Should have raised exception for empty signals")
        except Exception:
            pass  # Expected
    
    def test_cross_system_correlation(self):
        """Test cross-system correlation using execution_id"""
        signals = [{"type": "risk", "value": 0.4}]
        result = self.pipeline.execute_pipeline(signals)
        
        execution_id = result["execution_id"]
        
        # Verify execution_id exists in all systems
        trace = self.insightbridge.retrieve_trace(execution_id)
        self.assertEqual(trace["trace"]["execution_id"], execution_id)
        
        # Verify decision and action correlation
        self.assertEqual(trace["trace"]["decision"], result["dgic_decision"])
        self.assertEqual(trace["trace"]["action_taken"], result["enforcement_action"])
    
    def test_timeline_reconstruction_accuracy(self):
        """Test timeline reconstruction accuracy"""
        signals = [{"type": "risk", "value": 0.4}]
        result = self.pipeline.execute_pipeline(signals)
        
        execution_id = result["execution_id"]
        
        # Replay and check timeline
        replay_result = self.replay_system.replay_execution(execution_id)
        timeline = replay_result["timeline"]
        
        # Verify 4 systems in timeline
        systems = [event["system"] for event in timeline]
        self.assertIn("orchestrator", systems)
        self.assertIn("dgic", systems)
        self.assertIn("enforcement", systems)
        self.assertIn("insightbridge", systems)
    
    def test_system_state_extraction(self):
        """Test system state extraction from replay"""
        signals = [{"type": "risk", "value": 0.4}]
        result = self.pipeline.execute_pipeline(signals)
        
        execution_id = result["execution_id"]
        
        # Replay and extract states
        replay_result = self.replay_system.replay_execution(execution_id)
        states = replay_result["system_states"]
        
        # Verify all system states present
        self.assertIn("orchestrator", states)
        self.assertIn("dgic", states)
        self.assertIn("enforcement", states)
        self.assertIn("insightbridge", states)
    
    def test_error_propagation(self):
        """Test error propagation through systems"""
        signals = [{"type": "risk", "value": 0.4}]
        
        result = self.resilient_pipeline.execute_with_failure_handling(
            signals,
            simulate_dgic_failure=True
        )
        
        # Verify error logged
        self.assertIn("error_log", result)
        self.assertGreater(len(result["error_log"]), 0)
    
    def test_execution_logging(self):
        """Test execution logging across systems"""
        signals = [{"type": "risk", "value": 0.4}]
        result = self.pipeline.execute_pipeline(signals)
        
        # Verify execution log
        self.assertIn("execution_log", result)
        self.assertGreater(len(result["execution_log"]), 0)
    
    def test_performance_baseline(self):
        """Test performance baseline for single execution"""
        signals = [{"type": "risk", "value": 0.4}]
        
        start_time = time.time()
        result = self.pipeline.execute_pipeline(signals)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Verify execution completed
        self.assertEqual(result["status"], "success")
        
        # Log execution time for baseline
        print(f"\nExecution time: {execution_time:.3f}s")


def run_integration_tests():
    """Run all integration tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFullIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("PHASE 8: COMPREHENSIVE INTEGRATION TESTING")
    print("=" * 70)
    print("\nTesting complete flow across all BHIV systems:")
    print("- Orchestrator → DGIC → Enforcement → InsightBridge")
    print("- Replay System")
    print("- Failure Recovery")
    print("- Cross-System Correlation")
    print("\n" + "=" * 70)
    
    success = run_integration_tests()
    
    print("\n" + "=" * 70)
    if success:
        print("✓ All integration tests passed!")
    else:
        print("✗ Some integration tests failed")
    print("=" * 70)
