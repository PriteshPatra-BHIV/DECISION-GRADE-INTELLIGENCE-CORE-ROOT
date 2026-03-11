import threading


def run_parallel_proposals(adapter, threads=50):

    results = []

    def worker():
        action = adapter.propose_decision()
        results.append(action)

    thread_list = []

    for _ in range(threads):
        t = threading.Thread(target=worker)
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    return results