def test_10000_replay_stability(harness):

    baseline = harness.serialize_snapshot()

    for _ in range(10000):

        assert harness.serialize_snapshot() == baseline