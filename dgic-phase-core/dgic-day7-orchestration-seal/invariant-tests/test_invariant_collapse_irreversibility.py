import pytest
import sys
import os
import importlib.util

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, parent_dir)

collapse_path = os.path.join(parent_dir, "dgic-day3-collapse-irreversibility", "collapse_engine.py")
spec = importlib.util.spec_from_file_location("collapse_engine", collapse_path)
collapse_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collapse_module)

CollapseEngine = collapse_module.CollapseEngine
CollapseViolation = collapse_module.CollapseViolation


def test_illegal_collapse_blocked():
    engine = CollapseEngine()

    with pytest.raises(CollapseViolation):
        engine.collapse("Known", "X")