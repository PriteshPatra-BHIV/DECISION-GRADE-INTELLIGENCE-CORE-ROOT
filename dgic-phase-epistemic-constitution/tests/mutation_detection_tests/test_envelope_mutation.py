# test_envelope_mutation.py
import hashlib
import json


def hash_envelope(env):
    return hashlib.sha256(
        json.dumps(env, sort_keys=True).encode()
    ).hexdigest()


def test_envelope_mutation_detection():
    envelope = {
        "epistemic_state": "AMBIGUOUS",
        "entropy_score": 0.4
    }

    original_hash = hash_envelope(envelope)

    envelope["entropy_score"] = 0.8

    new_hash = hash_envelope(envelope)

    assert original_hash != new_hash