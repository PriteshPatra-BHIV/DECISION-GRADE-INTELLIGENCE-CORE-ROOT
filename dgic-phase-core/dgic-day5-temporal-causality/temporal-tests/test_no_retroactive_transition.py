import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from temporal_controller import (
    TemporalController,
    TemporalState,
    TemporalViolation,
)


def test_no_skip_forward():
    controller = TemporalController()

    # Cannot jump directly to Collapsed
    with pytest.raises(TemporalViolation):
        controller.transition(TemporalState.COLLAPSED)


def test_no_direct_archive_from_pre_observation():
    controller = TemporalController()

    # Cannot jump directly to Archived
    with pytest.raises(TemporalViolation):
        controller.transition(TemporalState.ARCHIVED)


def test_no_backward_after_archive():
    controller = TemporalController()

    controller.transition(TemporalState.OBSERVED)
    controller.transition(TemporalState.COLLAPSED)
    controller.transition(TemporalState.ARCHIVED)

    # Cannot move backward after archival
    with pytest.raises(TemporalViolation):
        controller.transition(TemporalState.COLLAPSED)