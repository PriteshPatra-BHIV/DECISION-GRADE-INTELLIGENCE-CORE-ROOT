import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from temporal_controller import (
    TemporalController,
    TemporalState,
    TemporalViolation,
)


def test_forward_progression():
    controller = TemporalController()

    controller.transition(TemporalState.OBSERVED)
    controller.transition(TemporalState.COLLAPSED)
    controller.transition(TemporalState.ARCHIVED)

    assert controller.current_state == TemporalState.ARCHIVED


def test_backward_transition_blocked():
    controller = TemporalController()

    controller.transition(TemporalState.OBSERVED)
    controller.transition(TemporalState.COLLAPSED)

    with pytest.raises(TemporalViolation):
        controller.transition(TemporalState.OBSERVED)


def test_archived_reentry_blocked():
    controller = TemporalController()

    controller.transition(TemporalState.OBSERVED)
    controller.transition(TemporalState.COLLAPSED)
    controller.transition(TemporalState.ARCHIVED)

    with pytest.raises(TemporalViolation):
        controller.transition(TemporalState.OBSERVED)