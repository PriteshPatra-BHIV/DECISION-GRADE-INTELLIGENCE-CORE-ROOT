"""
Phase 5: End-to-End Flow Implementation
Owner: Pritesh Patra

This module demonstrates ONE continuous flow:
Orchestrator → DGIC → Enforcement → InsightBridge

This is the complete BHIV pipeline integration.
"""

import uuid
import time
import json
from typing import Dict, List

# Import all integration clients
import sys
sys.path.append('.')

from orchestrator_dgic_integration import OrchestratorDGICClient
from enforcement_dgic_integration import EnforcementDGICClient
from insightbridge_dgic_integration import InsightBridgeDGICClient


class BHIVPipeline:
    """
    Complete BHIV pipeline integrating all systems.
    
    Flow:
    1. Orchestrator creates signals and calls DGIC
    2. DGIC processes signals and returns decision
    3. Enforcement consumes decision and executes action
    4. InsightBridge consumes trace for telemetry
    """
    
    def __init__(self, dgic_url: str = "http://localhost:8000"):
        """
        Initialize complete pipeline.
        
        Args:
            dgic_url: DGIC service URL
        """
        self.orchestrator = OrchestratorDGICClient(dgic_url=dgic_url)
        self.enforcement = EnforcementDGICClient(enable_override=True)
        self.insightbridge = InsightBridgeDGICClient()
        
        self.execution_log = []
    
    def execute_pipeline(
        self, 
        signals: List[Dict],
        execution_id: Optional[str] = None,
        enforcement_override: Optional[str] = None
    ) -> Dict:
        """
        Execute complete end-to-end pipeline.
        
        Args:
            signals: List of signal dictionaries
            execution_id: Optional execution ID (generated if not provided)
            enforcement_override: Optional enforcement override
            
        Returns:
            Dict with complete pipeline execution result
        """
        
        pipeline_start = time.time()
        
        # Generate execution_id if not provided
        if execution_id is None:
            execution_id = str(uuid.uuid4())
        
        print(f"\n{'='*80}")
        print(f"PIPELINE EXECUTION: {execution_id}")
        print(f"{'='*80}")
        
        # ===== STEP 1: Orchestrator → DGIC =====
        print("\n[STEP 1] Orchestrator → DGIC")
        print("-" * 80)
        
        try:
            dgic_response = self.orchestrator.evaluate_decision(
                signals=signals,
                execution_id=execution_id
            )
            
            print(f"✓ DGIC Decision: {dgic_response['decision']}")
            print(f"✓ Confidence: {dgic_response['confidence']}")
            print(f"✓ Epistemic State: {dgic_response['epistemic_state']}")
            print(f"✓ Execution Hash: {dgic_response['execution_hash'][:16]}...")
            
        except Exception as e:
            print(f"✗ DGIC Error: {e}")
            return {
                "success": False,
                "execution_id": execution_id,
                "error": f"DGIC failed: {str(e)}",
                "stage": "DGIC"
            }
        
        # ===== STEP 2: DGIC → Enforcement =====
        print("\n[STEP 2] DGIC → Enforcement")
        print("-" * 80)
        
        try:
            action = self.enforcement.map_decision_to_action(dgic_response)
            print(f"✓ Action Mapped: {action['action']}")
            
            enforcement_result = self.enforcement.execute_action(
                action,
                override=enforcement_override
            )
            
            print(f"✓ Enforcement Status: {enforcement_result['status']}")
            if enforcement_result.get('override_applied'):
                print(f"⚠ Override Applied: {enforcement_override}")
            
        except Exception as e:
            print(f"✗ Enforcement Error: {e}")
            return {
                "success": False,
                "execution_id": execution_id,
                "error": f"Enforcement failed: {str(e)}",
                "stage": "Enforcement",
                "dgic_response": dgic_response
            }
        
        # ===== STEP 3: DGIC → InsightBridge (Trace) =====
        print("\n[STEP 3] DGIC → InsightBridge (Trace)")
        print("-" * 80)
        
        # Simulate trace data (in real scenario, this comes from /dgic/trace endpoint)
        trace_data = self._generate_trace(signals, dgic_response)
        
        try:
            trace_verification = self.insightbridge.verify_trace(trace_data)
            print(f"✓ Trace Verified: {trace_verification['valid']}")
            
            trace_storage = self.insightbridge.store_trace(
                trace_data,
                verify_first=False  # Already verified
            )
            
            print(f"✓ Trace Stored: {trace_storage['stored']}")
            print(f"✓ Trace Hash: {trace_data['trace_hash'][:16]}...")
            
        except Exception as e:
            print(f"✗ InsightBridge Error: {e}")
            # InsightBridge failure is acceptable per contract
            print("⚠ Continuing despite InsightBridge failure (acceptable)")
        
        # ===== STEP 4: Cross-System Correlation =====
        print("\n[STEP 4] Cross-System Correlation")
        print("-" * 80)
        
        correlation = self.insightbridge.correlate_by_execution_id(execution_id)
        
        if correlation['found']:
            print(f"✓ Correlation Found")
            print(f"  - Input Signals: {len(correlation['input_signals'])}")
            print(f"  - Final Decision: {correlation['final_decision']}")
            print(f"  - Reasoning Steps: {correlation['reasoning_steps']}")
        
        # ===== Pipeline Complete =====
        pipeline_end = time.time()
        pipeline_duration = int((pipeline_end - pipeline_start) * 1000)
        
        print(f"\n{'='*80}")
        print(f"PIPELINE COMPLETE: {execution_id}")
        print(f"Total Duration: {pipeline_duration}ms")
        print(f"{'='*80}\n")
        
        # Build complete result
        result = {
            "success": True,
            "execution_id": execution_id,
            "pipeline_duration_ms": pipeline_duration,
            "orchestrator": {
                "signals_sent": len(signals),
                "dgic_response": dgic_response
            },
            "dgic": {
                "decision": dgic_response['decision'],
                "confidence": dgic_response['confidence'],
                "epistemic_state": dgic_response['epistemic_state'],
                "execution_hash": dgic_response['execution_hash']
            },
            "enforcement": {
                "action": action['action'],
                "status": enforcement_result['status'],
                "override_applied": enforcement_result.get('override_applied', False)
            },
            "insightbridge": {
                "trace_stored": trace_storage.get('stored', False),
                "trace_hash": trace_data.get('trace_hash'),
                "correlation_found": correlation.get('found', False)
            }
        }
        
        # Log execution
        self.execution_log.append(result)
        
        return result
    
    def _generate_trace(self, signals: List[Dict], dgic_response: Dict) -> Dict:
        """
        Generate trace data for InsightBridge.
        In production, this comes from /dgic/trace endpoint.
        """
        
        import hashlib
        
        current_time = int(time.time() * 1000)
        
        # Simplified trace generation
        trace_obj = {
            "execution_id": dgic_response['execution_id'],
            "timestamp": current_time,
            "input_signals": [
                {
                    "id": s['id'],
                    "type": s['type'],
                    "priority": s['priority'],
                    "timestamp": s['timestamp']
                }
                for s in signals
            ],
            "reasoning_trace": [
                {
                    "step": 1,
                    "operation": "signal_aggregation",
                    "result": {"signal_count": len(signals)},
                    "timestamp": current_time
                },
                {
                    "step": 2,
                    "operation": "state_computation",
                    "result": {
                        "state": dgic_response['epistemic_state'],
                        "confidence": dgic_response['confidence']
                    },
                    "timestamp": current_time + 10
                }
            ],
            "collapse_event": {
                "occurred": dgic_response['collapse_trigger'] != "none",
                "trigger": dgic_response['collapse_trigger'],
                "timestamp": current_time + 20,
                "selected_state": dgic_response['decision'] if dgic_response['collapse_trigger'] != "none" else None,
                "eliminated_states": [],
                "reason": f"Collapse triggered by {dgic_response['collapse_trigger']}" if dgic_response['collapse_trigger'] != "none" else "No collapse"
            },
            "final_state": {
                "decision": dgic_response['decision'],
                "confidence": dgic_response['confidence'],
                "epistemic_state": dgic_response['epistemic_state']
            },
            "execution_hash": dgic_response['execution_hash']
        }
        
        # Calculate trace hash
        trace_json = json.dumps(trace_obj, sort_keys=True, separators=(',', ':'))
        trace_hash = hashlib.sha256(trace_json.encode()).hexdigest()
        trace_obj['trace_hash'] = trace_hash
        
        return trace_obj
    
    def get_execution_log(self) -> List[Dict]:
        """Get complete execution log"""
        return self.execution_log
    
    def get_execution_summary(self, execution_id: str) -> Dict:
        """Get summary for specific execution"""
        for log in self.execution_log:
            if log['execution_id'] == execution_id:
                return log
        return {"found": False, "execution_id": execution_id}


# Convenience function for quick pipeline execution
def execute_bhiv_pipeline(signals: List[Dict], dgic_url: str = "http://localhost:8000") -> Dict:
    """
    Quick function to execute complete BHIV pipeline.
    
    Args:
        signals: List of signal dictionaries
        dgic_url: DGIC service URL
        
    Returns:
        Pipeline execution result
    """
    pipeline = BHIVPipeline(dgic_url=dgic_url)
    return pipeline.execute_pipeline(signals)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("BHIV END-TO-END PIPELINE DEMONSTRATION")
    print("="*80)
    print("\nThis demonstrates ONE continuous flow:")
    print("Orchestrator → DGIC → Enforcement → InsightBridge")
    print("\nNote: Requires DGIC service running at http://localhost:8000")
    print("="*80)
