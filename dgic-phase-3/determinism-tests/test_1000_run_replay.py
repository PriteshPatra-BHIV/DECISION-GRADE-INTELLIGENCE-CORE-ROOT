from replay_harness import replay_journal, ReplayViolation


def test_replay_stability(runs=1000):
    print(f"Running deterministic replay test ({runs} runs)...")

    reference_states, reference_hash = replay_journal()

    for i in range(runs):
        states, final_hash = replay_journal()

        if states != reference_states:
            raise ReplayViolation(
                f"State sequence mismatch on run {i}"
            )

        if final_hash != reference_hash:
            raise ReplayViolation(
                f"Hash mismatch on run {i}"
            )

    print("1000-run replay stability test PASSED.")
    print("Final deterministic hash:", reference_hash)


if __name__ == "__main__":
    try:
        test_replay_stability(1000)
    except ReplayViolation as e:
        print("Determinism test failed:", e)
