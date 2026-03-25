"""
Phase 6: Failure Flow Integration
Owner: Pritesh Patra

This module demonstrates failure handling across all systems:
- DGIC failure handling
- Enforcement failure handling
- Orchestrator failure handling
- System must fail safely, log correctly, not break chain
"""

import uuid
import time
import json
from typing import Dict, List, Optional
from enum import Enum

from end_to_end_pipeline import BHIVPipeline


class FailureType(Enum):
    """Types of failures that can be injected"""
    DGIC_UNREACHABLE = "dgic_unreachable"
    DGIC_TIMEOUT = "dgic_timeout"
    DGIC_INVALID_RESPONSE = "dgic_invalid_response"
    ENFORCEMENT_ERROR = "enforcement_error"
    INSIGHTBRIDGE_ERROR = "insightbridge_error"
    INVALID_SIGNALS = "invalid_signals"
    NETWORK_ERROR = "network_error"


class FailureInjector:
    """
    Injects failures into the pipeline for testing failure handling.
    """
    
    def __init__(self):
        self.failure_log = []
    
    def inject_failure(self, failure_type: FailureType, context: Dict) -> Dict:
        """
        Inject a failure and log it.
        
        Args:
            failure_type: Type of failure to inject
            context: Context information about the failure
            
        Returns:
            Dict with failure information
        """
        failure_entry = {
            "failure_type": failure_type.value,
            "timestamp": int(time.time() * 1000),
            "context": context,
            "handled": False
        }
        
        self.failure_log.append(failure_entry)
        
        return failure_entry
    
    def mark_handled(self, failure_entry: Dict):
        """Mark a failure as handled"""
        failure_entry["handled"] = True
    
    def get_failure_log(self) -> List[Dict]:
        """Get complete failure log"""
        return self.failure_log


class ResilientBHIVPipeline(BHIVPipeline):
    """
    Extended BHIV pipeline with failure handling capabilities.
    
    Demonstrates:
    - Graceful degradation
    - Error logging
    - Fail-safe behavior
    - Chain integrity maintenance
    """
    
    def __init__(self, dgic_url: str = "http://localhost:8000"):
        super().__init__(dgic_url)
        self.failure_injector = FailureInjector()
        self.failure_log = []
    
    def execute_with_failure_handling(
        self,
        signals: List[Dict],
        execution_id: Optional[str] = None,
        inject_failure: Optional[FailureType] = None
    ) -> Dict:
        """
        Execute pipeline with comprehensive failure handling.
        
        Args:
            signals: List of signal dictionaries
            execution_id: Optional execution ID
            inject_failure: Optional failure to inject for testing
            
        Returns:
            Dict with execution result including failure information
        """
        
        pipeline_start = time.time()
        
        if execution_id is None:
            execution_id = str(uuid.uuid4())
        
        print(f"\n{'='*80}")
        print(f"RESILIENT PIPELINE EXECUTION: {execution_id}")
        if inject_failure:
            print(f"⚠️  INJECTING FAILURE: {inject_failure.value}")
        print(f"{'='*80}")
        
        result = {
            "success": False,
            "execution_id": execution_id,
            "failures": [],
            "recovery_actions": []
        }
        
        # ===== STEP 1: Orchestrator → DGIC (with failure handling) =====
        print("\n[STEP 1] Orchestrator → DGIC (with failure handling)")
        print("-" * 80)
        
        dgic_response = None
        
        try:
            # Inject failure if requested
            if inject_failure == FailureType.DGIC_UNREACHABLE:
                raise ConnectionError("DGIC service unreachable")
            elif inject_failure == FailureType.DGIC_TIMEOUT:
                raise TimeoutError("DGIC request timed out")
            elif inject_failure == FailureType.INVALID_SIGNALS:
                raise ValueError("Invalid signal format")
            
            dgic_response = self.orchestrator.evaluate_decision(
                signals=signals,
                execution_id=execution_id
            )
            
            print(f"✓ DGIC Decision: {dgic_response['decision']}")
            print(f"✓ Confidence: {dgic_response['confidence']}")
            
        except ConnectionError as e:
            failure = self._handle_dgic_unreachable(execution_id, str(e))
            result["failures"].append(failure)
            result["recovery_actions"].append("Use cached decision or fail-safe")
            print(f"✗ DGIC Unreachable: {e}")
            print(f"⚡ Recovery: Failing safe - blocking operation")
            
            # Fail-safe: Create ERROR decision
            dgic_response = self._create_error_decision(execution_id)
            
        except TimeoutError as e:
            failure = self._handle_dgic_timeout(execution_id, str(e))
            result["failures"].append(failure)
            result["recovery_actions"].append("Retry or fail-safe")
            print(f"✗ DGIC Timeout: {e}")
            print(f"⚡ Recovery: Failing safe - blocking operation")
            
            dgic_response = self._create_error_decision(execution_id)
            
        except ValueError as e:
            failure = self._handle_invalid_input(execution_id, str(e))
            result["failures"].append(failure)
            result["recovery_actions"].append("Reject request")
            print(f"✗ Invalid Input: {e}")
            print(f"⚡ Recovery: Request rejected")
            
            return {
                "success": False,
                "execution_id": execution_id,
                "error": "Invalid input",
                "failures": result["failures"],
                "stage": "Input Validation"
            }
        
        except Exception as e:
            failure = self._handle_unexpected_error(execution_id, "DGIC", str(e))
            result["failures"].append(failure)
            print(f"✗ Unexpected Error: {e}")
            
            dgic_response = self._create_error_decision(execution_id)
        
        # ===== STEP 2: DGIC → Enforcement (with failure handling) =====
        print("\n[STEP 2] DGIC → Enforcement (with failure handling)")
        print("-" * 80)
        
        enforcement_result = None
        
        try:
            # Inject failure if requested
            if inject_failure == FailureType.ENFORCEMENT_ERROR:
                raise RuntimeError("Enforcement system error")
            
            action = self.enforcement.map_decision_to_action(dgic_response)
            print(f"✓ Action Mapped: {action['action']}")
            
            enforcement_result = self.enforcement.execute_action(action)
            print(f"✓ Enforcement Status: {enforcement_result['status']}")
            
        except RuntimeError as e:
            failure = self._handle_enforcement_error(execution_id, str(e))
            result["failures"].append(failure)
            result["recovery_actions"].append("Log failure and fail-safe")
            print(f"✗ Enforcement Error: {e}")
            print(f"⚡ Recovery: Logging failure, operation blocked")
            
            # Create fail-safe enforcement result
            enforcement_result = {
                "execution_id": execution_id,
                "action": "fail_safe",
                "status": "BLOCKED",
                "message": "Enforcement failed - operation blocked",
                "timestamp": int(time.time() * 1000),
                "override_applied": False,
                "error": str(e)
            }
            
        except Exception as e:
            failure = self._handle_unexpected_error(execution_id, "Enforcement", str(e))
            result["failures"].append(failure)
            print(f"✗ Unexpected Error: {e}")
            
            enforcement_result = {
                "execution_id": execution_id,
                "action": "fail_safe",
                "status": "BLOCKED",
                "message": "Unexpected error",
                "timestamp": int(time.time() * 1000),
                "override_applied": False
            }
        
        # ===== STEP 3: DGIC → InsightBridge (with failure handling) =====
        print("\n[STEP 3] DGIC → InsightBridge (with failure handling)")
        print("-" * 80)
        
        trace_storage = {"stored": False}
        
        try:
            # Inject failure if requested
            if inject_failure == FailureType.INSIGHTBRIDGE_ERROR:
                raise IOError("InsightBridge storage error")
            
            trace_data = self._generate_trace(signals, dgic_response)
            
            trace_verification = self.insightbridge.verify_trace(trace_data)
            print(f"✓ Trace Verified: {trace_verification['valid']}")
            
            trace_storage = self.insightbridge.store_trace(trace_data, verify_first=False)
            print(f"✓ Trace Stored: {trace_storage['stored']}")
            
        except IOError as e:
            failure = self._handle_insightbridge_error(execution_id, str(e))
            result["failures"].append(failure)
            result["recovery_actions"].append("Continue without trace (acceptable)")
            print(f"✗ InsightBridge Error: {e}")
            print(f"⚡ Recovery: Continuing without trace (acceptable per contract)")
            
            # InsightBridge failure is acceptable - continue
            
        except Exception as e:
            failure = self._handle_unexpected_error(execution_id, "InsightBridge", str(e))
            result["failures"].append(failure)
            print(f"✗ Unexpected Error: {e}")
            print(f"⚡ Recovery: Continuing without trace")
        
        # ===== Pipeline Complete (with failures handled) =====
        pipeline_end = time.time()
        pipeline_duration = int((pipeline_end - pipeline_start) * 1000)
        
        print(f"\n{'='*80}")
        print(f"RESILIENT PIPELINE COMPLETE: {execution_id}")
        print(f"Failures Encountered: {len(result['failures'])}")
        print(f"Recovery Actions Taken: {len(result['recovery_actions'])}")
        print(f"Total Duration: {pipeline_duration}ms")
        print(f"{'='*80}\n")
        
        # Build result
        result.update({
            "success": len(result["failures"]) == 0 or all(f.get("handled", False) for f in result["failures"]),
            "pipeline_duration_ms": pipeline_duration,
            "orchestrator": {
                "signals_sent": len(signals),
                "dgic_response": dgic_response
            },
            "dgic": {
                "decision": dgic_response.get('decision'),
                "confidence": dgic_response.get('confidence'),
                "epistemic_state": dgic_response.get('epistemic_state'),
                "execution_hash": dgic_response.get('execution_hash')
            },
            "enforcement": {
                "action": enforcement_result.get('action') if enforcement_result else None,
                "status": enforcement_result.get('status') if enforcement_result else None,
                "override_applied": enforcement_result.get('override_applied', False) if enforcement_result else False
            },
            "insightbridge": {
                "trace_stored": trace_storage.get('stored', False),
                "trace_hash": trace_storage.get('trace_hash')
            }
        })
        
        # Log execution
        self.failure_log.append(result)
        
        return result
    
    def _create_error_decision(self, execution_id: str) -> Dict:
        """Create ERROR decision for fail-safe"""
        return {
            "execution_id": execution_id,
            "timestamp": int(time.time() * 1000),
            "decision": "ERROR",
            "confidence": 0.0,
            "epistemic_state": "INSUFFICIENT",
            "collapse_trigger": "none",
            "execution_hash": "error_hash",
            "processing_time_ms": 0
        }
    
    def _handle_dgic_unreachable(self, execution_id: str, error: str) -> Dict:
        """Handle DGIC unreachable error"""
        return {
            "type": "DGIC_UNREACHABLE",
            "execution_id": execution_id,
            "error": error,
            "timestamp": int(time.time() * 1000),
            "handled": True,
            "recovery": "fail_safe"
        }
    
    def _handle_dgic_timeout(self, execution_id: str, error: str) -> Dict:
        """Handle DGIC timeout error"""
        return {
            "type": "DGIC_TIMEOUT",
            "execution_id": execution_id,
            "error": error,
            "timestamp": int(time.time() * 1000),
            "handled": True,
            "recovery": "fail_safe"
        }
    
    def _handle_invalid_input(self, execution_id: str, error: str) -> Dict:
        """Handle invalid input error"""
        return {
            "type": "INVALID_INPUT",
            "execution_id": execution_id,
            "error": error,
            "timestamp": int(time.time() * 1000),
            "handled": True,
            "recovery": "reject_request"
        }
    
    def _handle_enforcement_error(self, execution_id: str, error: str) -> Dict:
        """Handle enforcement error"""
        return {
            "type": "ENFORCEMENT_ERROR",
            "execution_id": execution_id,
            "error": error,
            "timestamp": int(time.time() * 1000),
            "handled": True,
            "recovery": "fail_safe"
        }
    
    def _handle_insightbridge_error(self, execution_id: str, error: str) -> Dict:
        """Handle InsightBridge error"""
        return {
            "type": "INSIGHTBRIDGE_ERROR",
            "execution_id": execution_id,
            "error": error,
            "timestamp": int(time.time() * 1000),
            "handled": True,
            "recovery": "continue_without_trace"
        }
    
    def _handle_unexpected_error(self, execution_id: str, component: str, error: str) -> Dict:
        """Handle unexpected error"""
        return {
            "type": "UNEXPECTED_ERROR",
            "component": component,
            "execution_id": execution_id,
            "error": error,
            "timestamp": int(time.time() * 1000),
            "handled": True,
            "recovery": "fail_safe"
        }
    
    def get_failure_log(self) -> List[Dict]:
        """Get complete failure log"""
        return self.failure_log


if __name__ == "__main__":
    print("\n" + "="*80)
    print("BHIV FAILURE FLOW DEMONSTRATION")
    print("="*80)
    print("\nThis demonstrates failure handling across all systems:")
    print("- DGIC failures")
    print("- Enforcement failures")
    print("- InsightBridge failures")
    print("- System fails safely, logs correctly, maintains chain integrity")
    print("="*80)
