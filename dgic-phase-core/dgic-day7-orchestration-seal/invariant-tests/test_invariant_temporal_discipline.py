import pytest
import sys
import os

# Add parent directory to path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, parent_dir)

# Import from directory with hyphens by using importlib
import importlib.util

temporal_path = os.path.join(parent_dir, "dgic-day5-temporal-causality", "temporal_controller.py")
spec = importlib.util.spec_from_file_location("temporal_controller", temporal_path)
temporal_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(temporal_module)

TemporalController = temporal_module.TemporalController
TemporalState = temporal_module.TemporalState
TemporalViolation = temporal_module.TemporalViolation


def test_backward_temporal_blocked():
    controller = TemporalController()

    controller.transition(TemporalState.OBSERVED)
    controller.transition(TemporalState.COLLAPSED)

    with pytest.raises(TemporalViolation):
        controller.transition(TemporalState.OBSERVED)