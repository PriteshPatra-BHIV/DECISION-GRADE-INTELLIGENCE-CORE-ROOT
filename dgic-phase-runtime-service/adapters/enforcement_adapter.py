class EnforcementAdapter:
    """
    Consumes DGIC epistemic state and produces enforcement signal.
    Does NOT mutate DGIC intelligence.
    """

    def evaluate_enforcement(self, dgic_response):

        state = dgic_response["epistemic_state"]
        confidence = dgic_response["confidence"]
        contradiction = dgic_response["contradiction_flag"]

        # Default enforcement signal
        decision = "ABSTAIN"

        if contradiction:
            decision = "REVIEW_REQUIRED"

        elif state == "CERTAIN" and confidence > 0.85:
            decision = "ENFORCE_ACTION"

        elif state == "AMBIGUOUS":
            decision = "DEFER_DECISION"

        return {
            "enforcement_decision": decision,
            "confidence": confidence,
            "source": "DGIC"
        }