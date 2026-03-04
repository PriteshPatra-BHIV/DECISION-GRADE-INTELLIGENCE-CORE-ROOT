import sys
sys.path.insert(0, 'src')
from envelope import create_envelope


def test_replay_chain_validation():
    e1 = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    e2 = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123", e1["envelope_hash"])
    e3 = create_envelope("KNOWN", 0.2, False, False, "def456", e2["envelope_hash"])
    
    assert e2["lineage_hash"] == e1["envelope_hash"]
    assert e3["lineage_hash"] == e2["envelope_hash"]


def test_replay_determinism_across_states():
    states = [
        ("AMBIGUOUS", 0.5, False, False, "abc123"),
        ("KNOWN", 0.2, False, False, "def456"),
        ("CONTRADICTORY", 0.8, True, False, "ghi789")
    ]
    
    chain1 = []
    parent = "GENESIS"
    for state in states:
        env = create_envelope(*state, parent)
        chain1.append(env)
        parent = env["envelope_hash"]
    
    chain2 = []
    parent = "GENESIS"
    for state in states:
        env = create_envelope(*state, parent)
        chain2.append(env)
        parent = env["envelope_hash"]
    
    for i in range(len(chain1)):
        assert chain1[i]["epistemic_state"] == chain2[i]["epistemic_state"]
        assert chain1[i]["lineage_hash"] == chain2[i]["lineage_hash"]


def test_parent_hash_chaining():
    e1 = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    e2 = create_envelope("AMBIGUOUS", 0.4, False, False, "abc124", e1["envelope_hash"])
    
    assert e2["lineage_hash"] == e1["envelope_hash"]
    assert e1["lineage_hash"] == "GENESIS"
