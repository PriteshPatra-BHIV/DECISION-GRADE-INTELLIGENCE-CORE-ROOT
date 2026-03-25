"""
DGIC → Enforcement Integration Layer
Owner: Pritesh Patra
Consumer: Rajaryan Verma (Enforcement Engine)

This module provides the integration interface for Enforcement to consume DGIC decisions.
"""

from typing import Dict, Optional, Callable
import time


class EnforcementDGICClient:
    """
    Client for Enforcement Engine to consume DGIC decisions and map to actions.
    
    Per integration contract Section 3.2:
    - DGIC provides intelligence, NOT authority
    - Enforcement owns final action decision
    - Enforcement can override DGIC (with logging)
    
    Usage:
        client = EnforcementDGICClient()
        action = client.map_decision_to_action(dgic_response)
        client.execute_action(action)
    """
    
    def __init__(self, enable_override: bool = True, log_callback: Optional[Callable] = None):
        """
        Initialize Enforcement client.
        
        Args:
            enable_override: Allow manual override of DGIC decisions
            log_callback: Optional callback for logging actions (func(log_entry: dict))
        """
        self.enable_override = enable_override
        self.log_callback = log_callback or self._default_logger
        self.action_log = []
    
    def map_decision_to_action(self, dgic_response: Dict) -> Dict:
        """
        Map DGIC decision to enforcement action.
        
        Per contract Section 3.2 Decision Mapping Matrix:
        - PROCEED → allow()
        - ESCALATE → escalate()
        - HOLD → delay()
        - REQUEST_MORE_DATA → request_input()
        - ERROR → fail_safe()
        
        Args:
            dgic_response: DGIC output matching integration_contract.md Section 3
            
        Returns:
            Dict containing:
                - execution_id: str
                - action: str (allow | escalate | delay | request_input | fail_safe)
                - decision: str (original DGIC decision)
                - confidence: float
                - epistemic_state: str
                - timestamp: int
                - source: str
        """
        
        # Extract DGIC output fields
        execution_id = dgic_response["execution_id"]
        decision = dgic_response["decision"]
        confidence = dgic_response["confidence"]
        epistemic_state = dgic_response["epistemic_state"]
        
        # Decision → Action mapping per contract
        action_map = {
            "PROCEED": "allow",
            "ESCALATE": "escalate",
            "HOLD": "delay",
            "REQUEST_MORE_DATA": "request_input",
            "ERROR": "fail_safe"
        }
        
        action = action_map.get(decision, "fail_safe")
        
        action_result = {
            "execution_id": execution_id,
            "action": action,
            "decision": decision,
            "confidence": confidence,
            "epistemic_state": epistemic_state,
            "timestamp": int(time.time() * 1000),
            "source": "DGIC",
            "override_applied": False
        }
        
        # Log action mapping
        self._log_action(action_result)
        
        return action_result
    
    def execute_action(self, action_result: Dict, override: Optional[str] = None) -> Dict:
        """
        Execute enforcement action with optional override.
        
        Args:
            action_result: Output from map_decision_to_action()
            override: Optional override action (allow | escalate | delay | request_input | fail_safe)
            
        Returns:
            Dict with execution status
        """
        
        execution_id = action_result["execution_id"]
        original_action = action_result["action"]
        
        # Apply override if provided and enabled
        if override and self.enable_override:
            if override not in ["allow", "escalate", "delay", "request_input", "fail_safe"]:
                raise ValueError(f"Invalid override action: {override}")
            
            self._log_override(execution_id, original_action, override)
            action_result["action"] = override
            action_result["override_applied"] = True
            action_result["original_action"] = original_action
        
        # Execute the action
        action = action_result["action"]
        
        if action == "allow":
            result = self._allow()
        elif action == "escalate":
            result = self._escalate()
        elif action == "delay":
            result = self._delay()
        elif action == "request_input":
            result = self._request_input()
        elif action == "fail_safe":
            result = self._fail_safe()
        else:
            result = self._fail_safe()
        
        execution_result = {
            "execution_id": execution_id,
            "action": action,
            "status": result["status"],
            "message": result["message"],
            "timestamp": int(time.time() * 1000),
            "override_applied": action_result.get("override_applied", False)
        }
        
        self._log_execution(execution_result)
        
        return execution_result
    
    def _allow(self) -> Dict:
        """Execute allow action - permit operation to proceed"""
        return {
            "status": "ALLOWED",
            "message": "Operation permitted to proceed"
        }
    
    def _escalate(self) -> Dict:
        """Execute escalate action - route to human/supervisor"""
        return {
            "status": "ESCALATED",
            "message": "Operation escalated to human supervisor"
        }
    
    def _delay(self) -> Dict:
        """Execute delay action - postpone decision"""
        return {
            "status": "DELAYED",
            "message": "Operation delayed pending additional data"
        }
    
    def _request_input(self) -> Dict:
        """Execute request_input action - request more signals"""
        return {
            "status": "INPUT_REQUESTED",
            "message": "Additional input requested from Orchestrator"
        }
    
    def _fail_safe(self) -> Dict:
        """Execute fail_safe action - block operation"""
        return {
            "status": "BLOCKED",
            "message": "Operation blocked due to error or safety concern"
        }
    
    def _log_action(self, action_result: Dict):
        """Log action mapping"""
        log_entry = {
            "type": "ACTION_MAPPING",
            "execution_id": action_result["execution_id"],
            "decision": action_result["decision"],
            "action": action_result["action"],
            "confidence": action_result["confidence"],
            "timestamp": action_result["timestamp"]
        }
        self.action_log.append(log_entry)
        self.log_callback(log_entry)
    
    def _log_override(self, execution_id: str, original_action: str, override_action: str):
        """Log override event"""
        log_entry = {
            "type": "OVERRIDE",
            "execution_id": execution_id,
            "original_action": original_action,
            "override_action": override_action,
            "timestamp": int(time.time() * 1000)
        }
        self.action_log.append(log_entry)
        self.log_callback(log_entry)
    
    def _log_execution(self, execution_result: Dict):
        """Log action execution"""
        log_entry = {
            "type": "EXECUTION",
            "execution_id": execution_result["execution_id"],
            "action": execution_result["action"],
            "status": execution_result["status"],
            "override_applied": execution_result["override_applied"],
            "timestamp": execution_result["timestamp"]
        }
        self.action_log.append(log_entry)
        self.log_callback(log_entry)
    
    def _default_logger(self, log_entry: Dict):
        """Default logger - prints to console"""
        pass  # Silent by default, can be overridden
    
    def get_action_log(self, execution_id: Optional[str] = None) -> list:
        """
        Retrieve action log.
        
        Args:
            execution_id: Optional filter by execution_id
            
        Returns:
            List of log entries
        """
        if execution_id:
            return [log for log in self.action_log if log.get("execution_id") == execution_id]
        return self.action_log


# Convenience function for quick integration
def consume_dgic_decision(dgic_response: Dict, override: Optional[str] = None) -> Dict:
    """
    Quick function to consume DGIC decision and execute action.
    
    Args:
        dgic_response: DGIC output
        override: Optional override action
        
    Returns:
        Execution result
    """
    client = EnforcementDGICClient()
    action = client.map_decision_to_action(dgic_response)
    return client.execute_action(action, override=override)
