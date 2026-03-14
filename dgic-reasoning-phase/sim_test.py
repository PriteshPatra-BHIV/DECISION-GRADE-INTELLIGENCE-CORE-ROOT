from multi_state_model import EpistemicState, EpistemicStateSet
from state_interference_model import StateInterferenceModel

s1 = EpistemicState(
    epistemic_state="THREAT",
    confidence=0.7,
    entropy=0.3,
    evidence_set=["S1"]
)

s2 = EpistemicState(
    epistemic_state="SENSOR_ERROR",
    confidence=0.3,
    entropy=0.6,
    evidence_set=["S2"]
)

state_set = EpistemicStateSet()

state_set.add_state(s1)
state_set.add_state(s2)

model = StateInterferenceModel()

result = model.apply_interference(state_set)

print(result.to_list())