from signal_injection_simulator import generate_signal


def stress_test_dgic(harness, iterations=500):

    snapshots = []

    for _ in range(iterations):

        signal = generate_signal()

        snapshot = harness.generate_snapshot()

        snapshots.append(snapshot)

    return snapshots