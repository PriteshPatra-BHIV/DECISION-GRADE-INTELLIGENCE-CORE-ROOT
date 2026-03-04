import sys
sys.path.insert(0, 'src')
from envelope import create_envelope
from boundary_guard import validate_source_authority, enforce_boundary
import pytest


def test_valid_source_authority():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    assert validate_source_authority(envelope) == True


def test_invalid_source_authority():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    envelope["source_module"] = "UNAUTHORIZED"
    assert validate_source_authority(envelope) == False


def test_boundary_enforcement():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    result = enforce_boundary(envelope)
    assert result == envelope


def test_boundary_rejection():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    envelope["source_module"] = "MALICIOUS"
    with pytest.raises(ValueError):
        enforce_boundary(envelope)


def test_dgic_authority_preservation():
    envelope = create_envelope("KNOWN", 0.2, False, False, "def456")
    assert envelope["source_module"] == "DGIC"
    assert validate_source_authority(envelope) == True
