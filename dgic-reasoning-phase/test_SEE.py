from multi_state_model import EpistemicState, EpistemicStateSet
from state_evolution_engine import StateEvolutionEngine

state1 = EpistemicState(
    epistemic_state="THREAT",
    confidence=0.6,
    entropy=0.4,
    evidence_set=["S1"]
)

state_set = EpistemicStateSet()
state_set.add_state(state1)

new_signal = {
    "signal_id": "S2",
    "type": "THREAT"
}

engine = StateEvolutionEngine()

result = engine.evolve_states(state_set, new_signal)

print(result.to_list())