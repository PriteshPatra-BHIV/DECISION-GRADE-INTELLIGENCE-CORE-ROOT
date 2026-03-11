import random


def generate_signal():

    states = ["AMBIGUOUS", "CERTAIN", "CONTRADICTORY"]

    return {
        "epistemic_state": random.choice(states),
        "entropy_score": random.random(),
        "contradiction_flag": random.choice([True, False]),
        "collapse_flag": False,
        "evidence_hash": "signal_" + str(random.randint(1, 1000))
    }