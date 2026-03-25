"""
DGIC → InsightBridge Integration Layer
Owner: Pritesh Patra
Consumer: Vijay Dhawan (InsightBridge)

This module provides the integration interface for InsightBridge to consume DGIC trace data.
"""

import hashlib
import json
from typing import Dict, Optional, List


class InsightBridgeDGICClient:
    """
    Client for InsightBridge to consume DGIC trace data.
    
    Per integration contract Section 4:
    - DGIC emits immutable trace data
    - InsightBridge stores traces without modification
    - Trace hash verification ensures integrity
    - Execution ID enables cross-system correlation
    
    Usage:
        client = InsightBridgeDGICClient()
        is_valid = client.verify_trace(trace_data)
        client.store_trace(trace_data)
    """
    
    def __init__(self, storage_callback: Optional[callable] = None):
        """
        Initialize InsightBridge client.
        
        Args:
            storage_callback: Optional callback for storing traces (func(trace: dict))
        """
        self.storage_callback = storage_callback or self._default_storage
        self.trace_store = []
    
    def verify_trace(self, trace_data: Dict) -> Dict:
        """
        Verify trace data integrity using trace_hash.
        
        Per contract Section 4.3:
        trace_hash = SHA256(JSON.stringify(entire_trace_object))
        
        Args:
            trace_data: DGIC trace output matching contract Section 4.1
            
        Returns:
            Dict containing:
                - valid: bool
                - execution_id: str
                - trace_hash_provided: str
                - trace_hash_computed: str
                - match: bool
        """
        
        execution_id = trace_data.get("execution_id")
        provided_hash = trace_data.get("trace_hash")
        
        if not provided_hash:
            return {
                "valid": False,
                "execution_id": execution_id,
                "error": "trace_hash missing from trace data"
            }
        
        # Compute trace hash (excluding trace_hash field itself)
        trace_copy = trace_data.copy()
        trace_copy.pop("trace_hash", None)
        
        # Deterministic JSON serialization
        trace_json = json.dumps(trace_copy, sort_keys=True, separators=(',', ':'))
        computed_hash = hashlib.sha256(trace_json.encode()).hexdigest()
        
        match = provided_hash == computed_hash
        
        return {
            "valid": match,
            "execution_id": execution_id,
            "trace_hash_provided": provided_hash,
            "trace_hash_computed": computed_hash,
            "match": match
        }
    
    def store_trace(self, trace_data: Dict, verify_first: bool = True) -> Dict:
        """
        Store trace data immutably.
        
        Args:
            trace_data: DGIC trace output
            verify_first: Whether to verify trace hash before storing
            
        Returns:
            Dict with storage result
        """
        
        execution_id = trace_data.get("execution_id")
        
        # Verify trace integrity if requested
        if verify_first:
            verification = self.verify_trace(trace_data)
            if not verification["valid"]:
                return {
                    "stored": False,
                    "execution_id": execution_id,
                    "error": "Trace verification failed",
                    "verification": verification
                }
        
        # Store trace immutably (no modifications)
        self.storage_callback(trace_data)
        self.trace_store.append(trace_data)
        
        return {
            "stored": True,
            "execution_id": execution_id,
            "timestamp": trace_data.get("timestamp"),
            "trace_hash": trace_data.get("trace_hash")
        }
    
    def retrieve_trace(self, execution_id: str) -> Optional[Dict]:
        """
        Retrieve trace by execution_id.
        
        Args:
            execution_id: UUID v4 execution identifier
            
        Returns:
            Trace data or None if not found
        """
        for trace in self.trace_store:
            if trace.get("execution_id") == execution_id:
                return trace
        return None
    
    def verify_execution_hash(self, trace_data: Dict, dgic_response: Dict) -> Dict:
        """
        Verify execution_hash matches between trace and DGIC response.
        
        Per contract Section 5.3:
        Trace execution_hash must match DGIC decision execution_hash
        
        Args:
            trace_data: DGIC trace output
            dgic_response: DGIC decision output
            
        Returns:
            Dict with verification result
        """
        
        trace_exec_hash = trace_data.get("execution_hash")
        response_exec_hash = dgic_response.get("execution_hash")
        
        match = trace_exec_hash == response_exec_hash
        
        return {
            "valid": match,
            "execution_id": trace_data.get("execution_id"),
            "trace_execution_hash": trace_exec_hash,
            "response_execution_hash": response_exec_hash,
            "match": match
        }
    
    def correlate_by_execution_id(self, execution_id: str) -> Dict:
        """
        Correlate all data for a given execution_id.
        
        Per contract Section 5.2:
        execution_id enables cross-system correlation
        
        Args:
            execution_id: UUID v4 execution identifier
            
        Returns:
            Dict with correlated data
        """
        
        trace = self.retrieve_trace(execution_id)
        
        if not trace:
            return {
                "found": False,
                "execution_id": execution_id,
                "error": "No trace found for execution_id"
            }
        
        return {
            "found": True,
            "execution_id": execution_id,
            "trace": trace,
            "input_signals": trace.get("input_signals", []),
            "final_decision": trace.get("final_state", {}).get("decision"),
            "confidence": trace.get("final_state", {}).get("confidence"),
            "epistemic_state": trace.get("final_state", {}).get("epistemic_state"),
            "collapse_occurred": trace.get("collapse_event", {}).get("occurred"),
            "reasoning_steps": len(trace.get("reasoning_trace", []))
        }
    
    def replay_verification(self, original_trace: Dict, replay_trace: Dict) -> Dict:
        """
        Verify replay consistency between original and replay traces.
        
        Per contract Section 5.3:
        Same input → identical trace_hash and execution_hash
        
        Args:
            original_trace: Original execution trace
            replay_trace: Replay execution trace
            
        Returns:
            Dict with replay verification result
        """
        
        original_trace_hash = original_trace.get("trace_hash")
        replay_trace_hash = replay_trace.get("trace_hash")
        
        original_exec_hash = original_trace.get("execution_hash")
        replay_exec_hash = replay_trace.get("execution_hash")
        
        trace_hash_match = original_trace_hash == replay_trace_hash
        exec_hash_match = original_exec_hash == replay_exec_hash
        
        return {
            "replay_valid": trace_hash_match and exec_hash_match,
            "trace_hash_match": trace_hash_match,
            "execution_hash_match": exec_hash_match,
            "original_trace_hash": original_trace_hash,
            "replay_trace_hash": replay_trace_hash,
            "original_execution_hash": original_exec_hash,
            "replay_execution_hash": replay_exec_hash
        }
    
    def get_all_traces(self, filter_by: Optional[Dict] = None) -> List[Dict]:
        """
        Retrieve all stored traces with optional filtering.
        
        Args:
            filter_by: Optional filter dict (e.g., {"decision": "ESCALATE"})
            
        Returns:
            List of traces
        """
        if not filter_by:
            return self.trace_store
        
        filtered = []
        for trace in self.trace_store:
            match = True
            for key, value in filter_by.items():
                if key == "decision":
                    if trace.get("final_state", {}).get("decision") != value:
                        match = False
                        break
                elif key == "epistemic_state":
                    if trace.get("final_state", {}).get("epistemic_state") != value:
                        match = False
                        break
                elif trace.get(key) != value:
                    match = False
                    break
            if match:
                filtered.append(trace)
        
        return filtered
    
    def _default_storage(self, trace_data: Dict):
        """Default storage - in-memory only"""
        pass  # Actual storage handled by trace_store list


# Convenience function for quick integration
def consume_dgic_trace(trace_data: Dict, verify: bool = True) -> Dict:
    """
    Quick function to consume and store DGIC trace.
    
    Args:
        trace_data: DGIC trace output
        verify: Whether to verify trace hash
        
    Returns:
        Storage result
    """
    client = InsightBridgeDGICClient()
    return client.store_trace(trace_data, verify_first=verify)
