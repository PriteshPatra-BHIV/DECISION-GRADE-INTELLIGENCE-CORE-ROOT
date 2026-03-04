import sys
sys.path.insert(0, 'src')
from envelope import create_envelope
from boundary_guard import detect_contamination, check_authority_escalation


def test_field_contamination_detection():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    modifications = ["epistemic_state", "entropy_score"]
    assert detect_contamination(envelope, modifications) == True


def test_safe_field_modification():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    modifications = ["metadata", "annotations"]
    assert detect_contamination(envelope, modifications) == False


def test_authority_escalation_detection():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    assert check_authority_escalation(envelope, "execute") == True
    assert check_authority_escalation(envelope, "enforce") == True
    assert check_authority_escalation(envelope, "inform") == False


def test_collapse_flag_protection():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, True, "abc123")
    assert check_authority_escalation(envelope, "collapse") == True


def test_downstream_mutation_prevention():
    envelope = create_envelope("KNOWN", 0.1, False, False, "xyz789")
    protected = ["envelope_hash", "evidence_hash", "collapse_flag"]
    assert detect_contamination(envelope, protected) == True
