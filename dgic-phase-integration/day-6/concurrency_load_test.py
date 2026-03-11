import threading


def test_concurrency_load(harness):

    results = []

    def worker():
        snapshot = harness.serialize_snapshot()
        results.append(snapshot)

    threads = []

    for _ in range(200):

        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(results) == 200