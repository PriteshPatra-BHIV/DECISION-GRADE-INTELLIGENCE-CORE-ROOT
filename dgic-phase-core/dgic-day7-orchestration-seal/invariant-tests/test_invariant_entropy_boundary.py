import pytest
import sys
import os
import importlib.util

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, parent_dir)

uncertainty_path = os.path.join(parent_dir, "dgic-day6-quantum-formalization", "uncertainty_model.py")
spec = importlib.util.spec_from_file_location("uncertainty_model", uncertainty_path)
uncertainty_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uncertainty_module)

UncertaintyModel = uncertainty_module.UncertaintyModel
UncertaintyViolation = uncertainty_module.UncertaintyViolation


def test_entropy_boundary_enforced():
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