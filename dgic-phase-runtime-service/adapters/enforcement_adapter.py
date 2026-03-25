class EnforcementAdapter:
    """
    Consumes DGIC decision and maps to enforcement actions.
    Per integration contract: DGIC provides intelligence, Enforcement owns action decision.
    """

    def map_decision_to_action(self, dgic_response):
        """
        Maps DGIC decision to enforcement action.
        
        Args:
            dgic_response: DGIC output matching integration_contract.md Section 3
            
        Returns:
            dict with action, confidence, execution_id for logging
        """
        decision = dgic_response["decision"]
        execution_id = dgic_response["execution_id"]
        confidence = dgic_response["confidence"]
        epistemic_state = dgic_response["epistemic_state"]
        
        # Decision mapping per contract Section 3.2
        action_map = {
            "PROCEED": "allow",
            "ESCALATE": "escalate",
            "HOLD": "delay",
            "REQUEST_MORE_DATA": "request_input",
            "ERROR": "fail_safe"
        }
        
        action = action_map.get(decision, "fail_safe")
        
        return {
            "execution_id": execution_id,
            "action": action,
            "decision": decision,
            "confidence": confidence,
            "epistemic_state": epistemic_state,
            "source": "DGIC"
        }
