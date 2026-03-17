import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from enforcement_adapter import EnforcementAdapter

adapter = EnforcementAdapter()

# Case 1: Ambiguous epistemic state
ambiguous = {
    "epistemic_state": "AMBIGUOUS",
    "confidence": 0.62,
    "contradiction_flag": False,
    "entropy_score": 0.38,
    "collapse_flag": False,
}
result = adapter.evaluate_enforcement(ambiguous)
assert result["enforcement_decision"] == "DEFER_DECISION", f"Expected DEFER_DECISION, got {result}"
print("Case 1 AMBIGUOUS:", result)

# Case 2: Contradiction state
contradiction = {
    "epistemic_state": "AMBIGUOUS",
    "confidence": 0.55,
    "contradiction_flag": True,
    "entropy_score": 0.45,
    "collapse_flag": False,
}
result = adapter.evaluate_enforcement(contradiction)
assert result["enforcement_decision"] == "REVIEW_REQUIRED", f"Expected REVIEW_REQUIRED, got {result}"
print("Case 2 CONTRADICTION:", result)

# Case 3: Forced certainty attack (value clamped to 1.0 by API, so confidence == 1.0)
forced_certainty = {
    "epistemic_state": "CERTAIN",
    "confidence": 1.0,
    "contradiction_flag": False,
    "entropy_score": 0.0,
    "collapse_flag": True,
}
result = adapter.evaluate_enforcement(forced_certainty)
assert result["enforcement_decision"] == "ENFORCE_ACTION", f"Expected ENFORCE_ACTION, got {result}"
print("Case 3 FORCED CERTAINTY:", result)

print("All enforcement test cases passed ✅")