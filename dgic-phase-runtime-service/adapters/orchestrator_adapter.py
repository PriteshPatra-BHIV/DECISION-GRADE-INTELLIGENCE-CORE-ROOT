import requests


class OrchestratorAdapter:
    """
    Simulates AI Being Orchestrator submitting action proposals to DGIC
    """

    def __init__(self, dgic_url="http://127.0.0.1:8000/dgic/evaluate"):
        self.dgic_url = dgic_url

    def evaluate_action(self, action_proposal, signals):
        request_data = {
            "signals": signals,
            "context": {"proposed_action": action_proposal},
            "source_system": "AI_BEING_ORCHESTRATOR",
            "prior_state": {},
        }

        try:
            response = requests.post(self.dgic_url, json=request_data, timeout=10)
            response.raise_for_status()
            dgic_result = response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "DGIC service unreachable", "action_proposal": action_proposal, "orchestrator_decision": "WAIT"}
        except requests.exceptions.Timeout:
            return {"error": "DGIC request timed out", "action_proposal": action_proposal, "orchestrator_decision": "WAIT"}
        except requests.exceptions.HTTPError as e:
            return {"error": str(e), "action_proposal": action_proposal, "orchestrator_decision": "WAIT"}

        decision = "WAIT"
        if dgic_result["epistemic_state"] == "CERTAIN" and dgic_result["confidence"] > 0.85:
            decision = "EXECUTE_ACTION"
        elif dgic_result["contradiction_flag"]:
            decision = "REVIEW_REQUIRED"

        return {
            "action_proposal": action_proposal,
            "dgic_result": dgic_result,
            "orchestrator_decision": decision,
        }