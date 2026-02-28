import json
import hashlib
from pathlib import Path
import os

MODULE_DIR = Path(__file__).parent
JOURNAL_FILE = MODULE_DIR / "state_journal.json"


class ReplayViolation(Exception):
    pass


def hash_event(event):
    event_copy = dict(event)
    original_hash = event_copy.pop("event_hash")

    serialized = json.dumps(event_copy, sort_keys=True)
    computed_hash = hashlib.sha256(serialized.encode()).hexdigest()

    if computed_hash != original_hash:
        raise ReplayViolation("Hash mismatch detected.")

    return computed_hash


def replay():
    if not JOURNAL_FILE.exists():
        raise ReplayViolation("Journal not found.")

    with open(JOURNAL_FILE, "r") as f:
        journal = json.load(f)

    previous_hash = "GENESIS"
    state_sequence = []

    for event in journal:
        if event["previous_hash"] != previous_hash:
            raise ReplayViolation("Hash chain broken.")

        computed_hash = hash_event(event)

        previous_hash = computed_hash
        state_sequence.append(event["target_state"])

    return state_sequence, previous_hash


if __name__ == "__main__":
    try:
        states, final_hash = replay()
        print("Replay successful.")
        print("State sequence:", states)
        print("Final hash:", final_hash)
    except ReplayViolation as e:
        print("Replay failed:", e)
