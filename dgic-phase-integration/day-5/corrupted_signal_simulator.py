import random


def generate_corrupted_signal():

    signals = [
        None,
        {},
        {"invalid": True},
        {"entropy_score": "NaN"},
        {"epistemic_state": 123},
        {"contradiction_flag": "error"}
    ]

    return random.choice(signals)