import hashlib
import json
import time


# STEP 1 — deterministic serialization
def deterministic_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


# STEP 1 — hash generator
def compute_hash(envelope):
    serialized = deterministic_json(envelope)
    return hashlib.sha256(serialized.encode()).hexdigest()


# STEP 2 — envelope builder
def create_envelope(state, parent_hash="GENESIS"):

    envelope = {
        "epistemic_state": state["epistemic_state"],
        "entropy_score": state["entropy_score"],
        "contradiction_flag": state["contradiction_flag"],
        "collapse_flag": state["collapse_flag"],
        "evidence_hash": state["evidence_hash"],
        "lineage_hash": parent_hash,
        "source_module": "DGIC",
        "schema_version": "1.0",
        "timestamp": int(time.time())
    }

    envelope["envelope_hash"] = compute_hash(envelope)

    return envelope


# STEP 3 — chain integrity test
def test_envelope_chain_integrity():

    state = {
        "epistemic_state": "AMBIGUOUS",
        "entropy_score": 0.5,
        "contradiction_flag": False,
        "collapse_flag": False,
        "evidence_hash": "abc123"
    }

    e1 = create_envelope(state)
    e2 = create_envelope(state, e1["envelope_hash"])
    e3 = create_envelope(state, e2["envelope_hash"])

    assert e2["lineage_hash"] == e1["envelope_hash"]
    assert e3["lineage_hash"] == e2["envelope_hash"]


# STEP 4 — tampering detection
def test_chain_tampering_detection():

    state = {
        "epistemic_state": "AMBIGUOUS",
        "entropy_score": 0.5,
        "contradiction_flag": False,
        "collapse_flag": False,
        "evidence_hash": "abc123"
    }

    e1 = create_envelope(state)
    e2 = create_envelope(state, e1["envelope_hash"])

    # tamper with envelope
    e1["entropy_score"] = 0.9

    tampered_hash = compute_hash(e1)

    assert tampered_hash != e1["envelope_hash"]


# STEP 5 — replay determinism
def test_replay_determinism():

    state = {
        "epistemic_state": "AMBIGUOUS",
        "entropy_score": 0.5,
        "contradiction_flag": False,
        "collapse_flag": False,
        "evidence_hash": "abc123"
    }

    e1 = create_envelope(state)
    e2 = create_envelope(state, e1["envelope_hash"])

    replay_e1 = create_envelope(state)
    replay_e2 = create_envelope(state, replay_e1["envelope_hash"])

    assert e1["epistemic_state"] == replay_e1["epistemic_state"]
    assert e2["lineage_hash"] == replay_e2["lineage_hash"]