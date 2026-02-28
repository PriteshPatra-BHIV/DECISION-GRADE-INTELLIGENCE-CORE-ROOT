import pytest
from uncertainty_model import (
    UncertaintyModel,
    UncertaintyViolation,
)


def test_entropy_reduction_without_evidence_blocked():
    model = UncertaintyModel({
        "Known": 0.25,
        "Inferred": 0.25,
        "Ambiguous": 0.25,
        "Unknown": 0.25,
    })

    with pytest.raises(UncertaintyViolation):
        model.update({
            "Known": 1.0,
            "Inferred": 0.0,
            "Ambiguous": 0.0,
            "Unknown": 0.0,
        }, evidence=False)


def test_entropy_reduction_with_evidence_allowed():
    model = UncertaintyModel({
        "Known": 0.25,
        "Inferred": 0.25,
        "Ambiguous": 0.25,
        "Unknown": 0.25,
    })

    new_entropy = model.update({
        "Known": 1.0,
        "Inferred": 0.0,
        "Ambiguous": 0.0,
        "Unknown": 0.0,
    }, evidence=True)

    assert new_entropy == 0