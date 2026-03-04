import sys
sys.path.insert(0, 'src')
from envelope import create_envelope, detect_mutation, validate_envelope


def test_hash_integrity_validation():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    assert validate_envelope(envelope) == True


def test_entropy_mutation_detection():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    envelope["entropy_score"] = 0.9
    assert detect_mutation(envelope) == True


def test_state_mutation_detection():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    envelope["epistemic_state"] = "KNOWN"
    assert detect_mutation(envelope) == True


def test_evidence_tampering_detection():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    envelope["evidence_hash"] = "tampered"
    assert detect_mutation(envelope) == True


def test_lineage_tampering_detection():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123", "parent_hash")
    envelope["lineage_hash"] = "fake_parent"
    assert detect_mutation(envelope) == True


def test_immutable_envelope():
    envelope = create_envelope("KNOWN", 0.1, False, False, "xyz789")
    original_hash = envelope["envelope_hash"]
    assert validate_envelope(envelope) == True
    assert envelope["envelope_hash"] == original_hash
