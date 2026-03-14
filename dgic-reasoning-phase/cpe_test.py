from multi_state_model import EpistemicState, EpistemicStateSet
from collapse_policy_engine import CollapsePolicyEngine

s1 = EpistemicState(
    epistemic_state="THREAT",
    confidence=0.88,
    entropy=0.15,
    evidence_set=["S1","S2"]
)

s2 = EpistemicState(
    epistemic_state="SENSOR_ERROR",
    confidence=0.10,
    entropy=0.7,
    evidence_set=["S3"]
)

state_set = EpistemicStateSet()

state_set.add_state(s1)
state_set.add_state(s2)

engine = CollapsePolicyEngine()

result = engine.evaluate_collapse(state_set)

print(result)