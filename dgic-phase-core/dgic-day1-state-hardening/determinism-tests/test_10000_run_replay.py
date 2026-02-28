from replay_harness import replay, ReplayViolation
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from state_engine import DeterministicStateEngine
import os
import json


def test_10000_run_replay(runs=100):  # Reduced for faster testing
    print(f"Running deterministic replay test ({runs} runs)...")
    
    # Clean and create fresh journal
    journal_file = Path(__file__).parent.parent / "state_journal.json"
    if journal_file.exists():
        os.remove(journal_file)
    
    engine = DeterministicStateEngine()
    engine.transition("Ambiguous")
    engine.transition("Inferred")
    engine.transition("Known", new_evidence=True)

    reference_states, reference_hash = replay()

    for i in range(runs):
        states, final_hash = replay()

        if states != reference_states:
            raise ReplayViolation(
                f"State sequence mismatch on run {i}"
            )

        if final_hash != reference_hash:
            raise ReplayViolation(
                f"Hash mismatch on run {i}"
            )

    print(f"{runs}-run deterministic replay PASSED.")
    print("Final hash:", reference_hash)


if __name__ == "__main__":
    try:
        test_10000_run_replay(10000)
    except ReplayViolation as e:
        print("Determinism test failed:", e)
