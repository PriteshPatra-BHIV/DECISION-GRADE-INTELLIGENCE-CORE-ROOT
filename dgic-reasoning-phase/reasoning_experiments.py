from multi_state_model import EpistemicState, EpistemicStateSet
from state_evolution_engine import StateEvolutionEngine
from state_interference_model import StateInterferenceModel
from collapse_policy_engine import CollapsePolicyEngine


def run_reasoning_experiment():

    # Initial hypotheses
    threat_state = EpistemicState(
        epistemic_state="THREAT",
        confidence=0.6,
        entropy=0.4,
        evidence_set=["S1"]
    )

    sensor_state = EpistemicState(
        epistemic_state="SENSOR_ERROR",
        confidence=0.3,
        entropy=0.7,
        evidence_set=["S2"]
    )

    state_set = EpistemicStateSet()

    state_set.add_state(threat_state)
    state_set.add_state(sensor_state)

    print("\nInitial Hypotheses:")
    print(state_set.to_list())

    # Step 1 — Evolution
    evolution_engine = StateEvolutionEngine()

    new_signal = {
        "signal_id": "S3",
        "type": "THREAT"
    }

    state_set = evolution_engine.evolve_states(state_set, new_signal)

    print("\nAfter Evidence Evolution:")
    print(state_set.to_list())

    # Step 2 — Interference
    interference_model = StateInterferenceModel()

    state_set = interference_model.apply_interference(state_set)

    print("\nAfter Hypothesis Interference:")
    print(state_set.to_list())

    # Step 3 — Collapse evaluation
    collapse_engine = CollapsePolicyEngine()

    collapse_result = collapse_engine.evaluate_collapse(state_set)

    print("\nCollapse Evaluation:")

    if collapse_result:
        print("Collapsed State →", collapse_result)
    else:
        print("No collapse. Ambiguity preserved.")


if __name__ == "__main__":
    run_reasoning_experiment()