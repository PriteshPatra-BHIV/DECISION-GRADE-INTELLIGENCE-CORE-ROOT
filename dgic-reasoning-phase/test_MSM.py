from multi_state_model import EpistemicState, EpistemicStateSet

s1 = EpistemicState(
    epistemic_state="THREAT",
    confidence=0.7,
    entropy=0.3,
    evidence_set=["S1", "S2"]
)

s2 = EpistemicState(
    epistemic_state="SENSOR_ERROR",
    confidence=0.2,
    entropy=0.8,
    evidence_set=["S3"]
)

state_set = EpistemicStateSet()

state_set.add_state(s1)
state_set.add_state(s2)

print(state_set.to_list())