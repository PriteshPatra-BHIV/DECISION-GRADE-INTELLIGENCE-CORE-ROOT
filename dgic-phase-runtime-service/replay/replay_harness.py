import requests
import hashlib
import sys

DGIC_URL = "http://127.0.0.1:8000/dgic/evaluate"

signals = [
    {
        "signal_id": "S1",
        "type": "THREAT",
        "value": 0.6,
    }
]


def run_replay_test():
    results = []

    for i in range(10000):
        request_data = {
            "signals": signals,
            "context": {},
            "source_system": "REPLAY_TEST",
            "prior_state": {},
        }

        try:
            response = requests.post(DGIC_URL, json=request_data, timeout=10)
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            print(f"Request failed on run {i}: {e}")
            sys.exit(1)

        result_hash = hashlib.sha256(str(result).encode()).hexdigest()
        results.append(result_hash)

    unique_hashes = set(results)

    print("Total Runs:", len(results))
    print("Unique Output Hashes:", len(unique_hashes))

    if len(unique_hashes) == 1:
        print("Deterministic Replay Verified ✅")
        sys.exit(0)
    else:
        print("Replay Drift Detected ❌")
        sys.exit(1)


if __name__ == "__main__":
    run_replay_test()