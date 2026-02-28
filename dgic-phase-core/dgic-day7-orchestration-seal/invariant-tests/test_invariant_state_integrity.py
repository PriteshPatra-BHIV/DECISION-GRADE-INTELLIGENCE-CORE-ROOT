import pytest
import sys
import os
import importlib.util

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, parent_dir)

state_path = os.path.join(parent_dir, "dgic-day1-state-hardening", "state_engine.py")
spec = importlib.util.spec_from_file_location("state_engine", state_path)
state_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state_module)

DeterministicStateEngine = state_module.DeterministicStateEngine
StateViolation = state_module.StateViolation


def test_illegal_promotion_blocked():
    engine = DeterministicStateEngine()

    with pytest.raises(StateViolation):
        engine.transition("Known")