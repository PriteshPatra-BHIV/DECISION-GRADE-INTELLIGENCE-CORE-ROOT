import sys
sys.path.insert(0, 'src')
from envelope import create_envelope
from schema_validator import validate_schema_version, reject_incompatible_schema, validate_against_schema
import pytest


def test_schema_version_validation():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    assert validate_schema_version(envelope, "1.0") == True


def test_schema_version_mismatch():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    envelope["schema_version"] = "2.0"
    assert validate_schema_version(envelope, "1.0") == False


def test_incompatible_schema_rejection():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    envelope["schema_version"] = "2.0"
    with pytest.raises(ValueError):
        reject_incompatible_schema(envelope)


def test_schema_field_validation():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    assert validate_against_schema(envelope) == True


def test_missing_required_field():
    envelope = create_envelope("AMBIGUOUS", 0.5, False, False, "abc123")
    del envelope["epistemic_state"]
    assert validate_against_schema(envelope) == False
