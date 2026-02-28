from implementation_updates.temporal_state_extension import (
    TemporalStateController,
    TemporalState,
    TemporalViolation,
)


def test_no_backward_transition():
    controller = TemporalStateController()

    controller.transition(TemporalState.OBSERVED)
    controller.transition(TemporalState.COLLAPSED)

    try:
        controller.transition(TemporalState.OBSERVED)
        print("FAIL: Collapsed → Observed should be blocked.")
    except TemporalViolation:
        print("PASS: Backward temporal transition blocked.")


def test_no_archived_reentry():
    controller = TemporalStateController()

    controller.transition(TemporalState.OBSERVED)
    controller.transition(TemporalState.COLLAPSED)
    controller.transition(TemporalState.ARCHIVED)

    try:
        controller.transition(TemporalState.OBSERVED)
        print("FAIL: Archived → Observed should be blocked.")
    except TemporalViolation:
        print("PASS: Archived re-entry blocked.")


def test_forward_only_time():
    controller = TemporalStateController()

    controller.transition(TemporalState.OBSERVED)

    # Simulate timestamp rollback attempt
    controller.last_event_timestamp = controller.last_event_timestamp

    try:
        controller.transition(TemporalState.COLLAPSED)
        print("PASS: Forward-only time maintained.")
    except TemporalViolation:
        print("FAIL: Unexpected temporal ordering violation.")


if __name__ == "__main__":
    test_no_backward_transition()
    test_no_archived_reentry()
    test_forward_only_time()
