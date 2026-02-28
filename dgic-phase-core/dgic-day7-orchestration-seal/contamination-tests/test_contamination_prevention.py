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

collapse_path = os.path.join(parent_dir, "dgic-day3-collapse-irreversibility", "collapse_engine.py")
spec2 = importlib.util.spec_from_file_location("collapse_engine", collapse_path)
collapse_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(collapse_module)

StateEngine = state_module.DeterministicStateEngine
CollapseEngine = collapse_module.CollapseEngine
CollapseViolation = collapse_module.CollapseViolation
StateViolation = state_module.StateViolation


def test_contamination_illegal_transition_blocked():
    """Verify downstream cannot trigger illegal state transitions"""
    engine = StateEngine()
    
    with pytest.raises(StateViolation):
        engine.transition("Known")


def test_contamination_collapse_requires_evidence():
    """Verify downstream cannot collapse without evidence"""
    engine = CollapseEngine()
    
    with pytest.raises(CollapseViolation):
        engine.collapse("Ambiguous", None)


def test_contamination_no_authority_assumption():
    """Verify core does not assume decision authority"""
    engine = StateEngine()
    
    assert not hasattr(engine, "make_decision")
    assert not hasattr(engine, "execute_action")
    assert not hasattr(engine, "enforce_policy")


def test_contamination_evidence_required_for_certainty():
    """Verify system requires evidence for certainty increase"""
    engine = StateEngine()
    
    # Transition to Known requires evidence
    with pytest.raises(StateViolation):
        engine.transition("Known", new_evidence=False)
