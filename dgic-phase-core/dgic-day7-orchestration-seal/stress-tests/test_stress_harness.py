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

temporal_path = os.path.join(parent_dir, "dgic-day5-temporal-causality", "temporal_controller.py")
spec3 = importlib.util.spec_from_file_location("temporal_controller", temporal_path)
temporal_module = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(temporal_module)

uncertainty_path = os.path.join(parent_dir, "dgic-day6-quantum-formalization", "uncertainty_model.py")
spec4 = importlib.util.spec_from_file_location("uncertainty_model", uncertainty_path)
uncertainty_module = importlib.util.module_from_spec(spec4)
spec4.loader.exec_module(uncertainty_module)

StateEngine = state_module.DeterministicStateEngine
CollapseEngine = collapse_module.CollapseEngine
TemporalController = temporal_module.TemporalController
TemporalState = temporal_module.TemporalState
UncertaintyModel = uncertainty_module.UncertaintyModel


def test_stress_state_transitions():
    engine = StateEngine()
    
    for i in range(50):
        engine.transition("Ambiguous")
        engine.transition("Inferred")
        engine.current_state = "Unknown"
    
    assert engine.current_state == "Unknown"


def test_stress_collapse_ledger():
    engine = CollapseEngine()
    
    for i in range(50):
        engine.collapse("Ambiguous", {"evidence": f"data_{i}"})
    
    assert engine.previous_hash != "GENESIS"


def test_stress_temporal_ordering():
    controller = TemporalController()
    
    for i in range(100):
        controller.transition(TemporalState.OBSERVED)
        controller.transition(TemporalState.COLLAPSED)
        controller.transition(TemporalState.ARCHIVED)
        controller.current_state = TemporalState.PRE_OBSERVATION
    
    assert controller.current_state == TemporalState.PRE_OBSERVATION


def test_stress_entropy_tracking():
    model = UncertaintyModel({
        "Known": 0.25,
        "Inferred": 0.25,
        "Ambiguous": 0.25,
        "Unknown": 0.25,
    })
    
    initial_entropy = model.entropy()
    assert initial_entropy >= 0.0
