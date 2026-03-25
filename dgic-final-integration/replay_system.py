"""
Phase 7: Replay Across Systems
Comprehensive replay system for reconstructing and verifying execution flows
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import hashlib


class ReplayStatus(Enum):
    """Status of replay verification"""
    VERIFIED = "verified"
    HASH_MISMATCH = "hash_mismatch"
    INCOMPLETE = "incomplete"
    CORRUPTED = "corrupted"


class SystemState(Enum):
    """State of each system in the replay"""
    ORCHESTRATOR = "orchestrator"
    DGIC = "dgic"
    ENFORCEMENT = "enforcement"
    INSIGHTBRIDGE = "insightbridge"


class ReplaySystem:
    """
    Replay system for reconstructing and verifying execution flows across BHIV systems.
    Supports full replay, partial replay, and verification of execution integrity.
    """
    
    def __init__(self, insightbridge_client):
        """
        Initialize replay system with InsightBridge client for trace retrieval.
        
        Args:
            insightbridge_client: InsightBridgeDGICClient instance
        """
        self.insightbridge = insightbridge_client
        self.replay_cache = {}
    
    def replay_execution(self, execution_id: str) -> Dict[str, Any]:
        """
        Replay complete execution flow for given execution_id.
        
        Args:
            execution_id: UUID of execution to replay
            
        Returns:
            Dict containing:
                - execution_id: str
                - replay_status: ReplayStatus
                - timeline: List of events in chronological order
                - system_states: Dict of states for each system
                - verification: Dict of verification results
                - errors: List of any errors encountered
        """
        result = {
            "execution_id": execution_id,
            "replay_status": None,
            "timeline": [],
            "system_states": {},
            "verification": {},
            "errors": []
        }
        
        try:
            # Retrieve trace from InsightBridge
            trace_data = self.insightbridge.retrieve_trace(execution_id)
            
            if not trace_data:
                result["replay_status"] = ReplayStatus.INCOMPLETE.value
                result["errors"].append("No trace found for execution_id")
                return result
            
            # Verify trace hash
            hash_valid = self.insightbridge.verify_execution_hash(execution_id)
            if not hash_valid:
                result["replay_status"] = ReplayStatus.HASH_MISMATCH.value
                result["errors"].append("Trace hash verification failed")
            
            # Reconstruct timeline
            result["timeline"] = self._reconstruct_timeline(trace_data)
            
            # Extract system states
            result["system_states"] = self._extract_system_states(trace_data)
            
            # Verify execution integrity
            result["verification"] = self._verify_execution_integrity(trace_data)
            
            # Determine final status
            if hash_valid and result["verification"]["integrity_valid"]:
                result["replay_status"] = ReplayStatus.VERIFIED.value
            elif not hash_valid:
                result["replay_status"] = ReplayStatus.HASH_MISMATCH.value
            else:
                result["replay_status"] = ReplayStatus.CORRUPTED.value
            
            # Cache replay result
            self.replay_cache[execution_id] = result
            
        except Exception as e:
            result["replay_status"] = ReplayStatus.CORRUPTED.value
            result["errors"].append(f"Replay failed: {str(e)}")
        
        return result
    
    def replay_batch(self, execution_ids: List[str]) -> Dict[str, Any]:
        """
        Replay multiple executions in batch.
        
        Args:
            execution_ids: List of execution IDs to replay
            
        Returns:
            Dict containing:
                - total: int
                - verified: int
                - failed: int
                - results: List of replay results
        """
        results = []
        verified_count = 0
        failed_count = 0
        
        for exec_id in execution_ids:
            replay_result = self.replay_execution(exec_id)
            results.append(replay_result)
            
            if replay_result["replay_status"] == ReplayStatus.VERIFIED.value:
                verified_count += 1
            else:
                failed_count += 1
        
        return {
            "total": len(execution_ids),
            "verified": verified_count,
            "failed": failed_count,
            "results": results
        }
    
    def replay_time_range(self, start_time: str, end_time: str) -> Dict[str, Any]:
        """
        Replay all executions within a time range.
        
        Args:
            start_time: ISO format start time
            end_time: ISO format end time
            
        Returns:
            Dict containing replay results for all executions in range
        """
        # Get all execution IDs in time range from InsightBridge
        execution_ids = self._get_executions_in_range(start_time, end_time)
        
        return self.replay_batch(execution_ids)
    
    def verify_decision_chain(self, execution_id: str) -> Dict[str, Any]:
        """
        Verify the decision chain integrity for an execution.
        
        Args:
            execution_id: UUID of execution
            
        Returns:
            Dict containing:
                - execution_id: str
                - chain_valid: bool
                - signal_to_decision: bool (Orchestrator → DGIC valid)
                - decision_to_action: bool (DGIC → Enforcement valid)
                - action_to_trace: bool (Enforcement → InsightBridge valid)
                - errors: List of validation errors
        """
        result = {
            "execution_id": execution_id,
            "chain_valid": False,
            "signal_to_decision": False,
            "decision_to_action": False,
            "action_to_trace": False,
            "errors": []
        }
        
        try:
            trace_data = self.insightbridge.retrieve_trace(execution_id)
            
            if not trace_data:
                result["errors"].append("No trace found")
                return result
            
            trace = trace_data.get("trace", {})
            
            # Verify signal → decision
            if trace.get("execution_id") == execution_id:
                result["signal_to_decision"] = True
            else:
                result["errors"].append("execution_id mismatch in trace")
            
            # Verify decision → action
            decision = trace.get("decision")
            action = trace.get("action_taken")
            
            if self._validate_decision_action_mapping(decision, action):
                result["decision_to_action"] = True
            else:
                result["errors"].append(f"Invalid decision-action mapping: {decision} → {action}")
            
            # Verify action → trace
            if trace.get("trace_hash"):
                result["action_to_trace"] = True
            else:
                result["errors"].append("Missing trace hash")
            
            # Overall chain validity
            result["chain_valid"] = (
                result["signal_to_decision"] and
                result["decision_to_action"] and
                result["action_to_trace"]
            )
            
        except Exception as e:
            result["errors"].append(f"Chain verification failed: {str(e)}")
        
        return result
    
    def compare_executions(self, execution_id_1: str, execution_id_2: str) -> Dict[str, Any]:
        """
        Compare two executions to identify differences.
        
        Args:
            execution_id_1: First execution ID
            execution_id_2: Second execution ID
            
        Returns:
            Dict containing comparison results
        """
        replay_1 = self.replay_execution(execution_id_1)
        replay_2 = self.replay_execution(execution_id_2)
        
        return {
            "execution_1": execution_id_1,
            "execution_2": execution_id_2,
            "status_match": replay_1["replay_status"] == replay_2["replay_status"],
            "timeline_length_match": len(replay_1["timeline"]) == len(replay_2["timeline"]),
            "decision_match": self._extract_decision(replay_1) == self._extract_decision(replay_2),
            "action_match": self._extract_action(replay_1) == self._extract_action(replay_2),
            "differences": self._identify_differences(replay_1, replay_2)
        }
    
    def audit_trail(self, execution_id: str) -> Dict[str, Any]:
        """
        Generate complete audit trail for an execution.
        
        Args:
            execution_id: UUID of execution
            
        Returns:
            Dict containing complete audit trail with timestamps, actors, and actions
        """
        replay_result = self.replay_execution(execution_id)
        
        audit = {
            "execution_id": execution_id,
            "audit_timestamp": datetime.utcnow().isoformat(),
            "replay_status": replay_result["replay_status"],
            "events": [],
            "summary": {}
        }
        
        # Build audit events from timeline
        for event in replay_result["timeline"]:
            audit["events"].append({
                "timestamp": event.get("timestamp"),
                "system": event.get("system"),
                "action": event.get("action"),
                "details": event.get("details")
            })
        
        # Generate summary
        audit["summary"] = {
            "total_events": len(audit["events"]),
            "systems_involved": list(replay_result["system_states"].keys()),
            "verification_status": replay_result["verification"],
            "errors": replay_result["errors"]
        }
        
        return audit
    
    def _reconstruct_timeline(self, trace_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Reconstruct chronological timeline from trace data"""
        timeline = []
        trace = trace_data.get("trace", {})
        
        # Orchestrator signal creation
        timeline.append({
            "timestamp": trace.get("timestamp"),
            "system": SystemState.ORCHESTRATOR.value,
            "action": "signal_created",
            "details": {
                "signals": trace.get("signals", []),
                "execution_id": trace.get("execution_id")
            }
        })
        
        # DGIC decision evaluation
        timeline.append({
            "timestamp": trace.get("timestamp"),
            "system": SystemState.DGIC.value,
            "action": "decision_evaluated",
            "details": {
                "decision": trace.get("decision"),
                "confidence": trace.get("confidence"),
                "reasoning": trace.get("reasoning")
            }
        })
        
        # Enforcement action execution
        timeline.append({
            "timestamp": trace.get("timestamp"),
            "system": SystemState.ENFORCEMENT.value,
            "action": "action_executed",
            "details": {
                "action_taken": trace.get("action_taken"),
                "decision": trace.get("decision")
            }
        })
        
        # InsightBridge trace storage
        timeline.append({
            "timestamp": trace_data.get("stored_at"),
            "system": SystemState.INSIGHTBRIDGE.value,
            "action": "trace_stored",
            "details": {
                "trace_hash": trace.get("trace_hash"),
                "execution_id": trace.get("execution_id")
            }
        })
        
        return timeline
    
    def _extract_system_states(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract state of each system from trace"""
        trace = trace_data.get("trace", {})
        
        return {
            SystemState.ORCHESTRATOR.value: {
                "signals": trace.get("signals", []),
                "execution_id": trace.get("execution_id")
            },
            SystemState.DGIC.value: {
                "decision": trace.get("decision"),
                "confidence": trace.get("confidence"),
                "reasoning": trace.get("reasoning")
            },
            SystemState.ENFORCEMENT.value: {
                "action_taken": trace.get("action_taken"),
                "status": "executed"
            },
            SystemState.INSIGHTBRIDGE.value: {
                "trace_hash": trace.get("trace_hash"),
                "stored": True,
                "stored_at": trace_data.get("stored_at")
            }
        }
    
    def _verify_execution_integrity(self, trace_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify integrity of execution"""
        trace = trace_data.get("trace", {})
        
        integrity_checks = {
            "execution_id_present": bool(trace.get("execution_id")),
            "decision_present": bool(trace.get("decision")),
            "action_present": bool(trace.get("action_taken")),
            "trace_hash_present": bool(trace.get("trace_hash")),
            "signals_present": bool(trace.get("signals")),
            "timestamp_present": bool(trace.get("timestamp"))
        }
        
        integrity_checks["integrity_valid"] = all(integrity_checks.values())
        
        return integrity_checks
    
    def _validate_decision_action_mapping(self, decision: str, action: str) -> bool:
        """Validate decision-to-action mapping per contract"""
        valid_mappings = {
            "PROCEED": "allow",
            "ESCALATE": "escalate",
            "HOLD": "delay",
            "REQUEST_MORE_DATA": "request_input",
            "ERROR": "fail_safe"
        }
        
        return valid_mappings.get(decision) == action
    
    def _get_executions_in_range(self, start_time: str, end_time: str) -> List[str]:
        """Get execution IDs within time range from InsightBridge"""
        # This would query InsightBridge for executions in time range
        # For now, return empty list as placeholder
        return []
    
    def _extract_decision(self, replay_result: Dict[str, Any]) -> Optional[str]:
        """Extract decision from replay result"""
        return replay_result.get("system_states", {}).get(SystemState.DGIC.value, {}).get("decision")
    
    def _extract_action(self, replay_result: Dict[str, Any]) -> Optional[str]:
        """Extract action from replay result"""
        return replay_result.get("system_states", {}).get(SystemState.ENFORCEMENT.value, {}).get("action_taken")
    
    def _identify_differences(self, replay_1: Dict[str, Any], replay_2: Dict[str, Any]) -> List[str]:
        """Identify differences between two replay results"""
        differences = []
        
        decision_1 = self._extract_decision(replay_1)
        decision_2 = self._extract_decision(replay_2)
        if decision_1 != decision_2:
            differences.append(f"Decision: {decision_1} vs {decision_2}")
        
        action_1 = self._extract_action(replay_1)
        action_2 = self._extract_action(replay_2)
        if action_1 != action_2:
            differences.append(f"Action: {action_1} vs {action_2}")
        
        status_1 = replay_1.get("replay_status")
        status_2 = replay_2.get("replay_status")
        if status_1 != status_2:
            differences.append(f"Status: {status_1} vs {status_2}")
        
        return differences
