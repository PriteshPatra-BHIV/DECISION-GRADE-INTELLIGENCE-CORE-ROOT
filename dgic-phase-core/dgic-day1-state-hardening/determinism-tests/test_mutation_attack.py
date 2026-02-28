import json
from pathlib import Path
from replay_harness import replay, ReplayViolation

JOURNAL_FILE = Path("state_journal.json")


def test_mutation_attack():
    if not JOURNAL_FILE.exists():
        print("No journal found. Run state transitions first.")
        return

    # Load original journal
    with open(JOURNAL_FILE, "r") as f:
        journal = json.load(f)

    if not journal:
        print("Journal empty. Nothing to mutate.")
        return

    # Mutate first entry
    journal[0]["target_state"] = "Known"

    # Save tampered journal
    with open(JOURNAL_FILE, "w") as f:
        json.dump(journal, f, indent=4)

    # Replay should fail
    try:
        replay()
        print("FAIL: Mutation not detected.")
    except ReplayViolation:
        print("PASS: Mutation detected successfully.")


if __name__ == "__main__":
    test_mutation_attack()
