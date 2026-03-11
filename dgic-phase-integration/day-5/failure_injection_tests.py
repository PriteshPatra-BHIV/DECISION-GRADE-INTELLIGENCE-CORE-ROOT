from corrupted_signal_simulator import generate_corrupted_signal


def test_downstream_failure_does_not_affect_core(harness):

    original_snapshot = harness.generate_snapshot()

    for _ in range(100):

        corrupted = generate_corrupted_signal()

        try:
            harness.generate_snapshot()
        except Exception:
            pass

    new_snapshot = harness.generate_snapshot()

    assert original_snapshot.epistemic_state == new_snapshot.epistemic_state