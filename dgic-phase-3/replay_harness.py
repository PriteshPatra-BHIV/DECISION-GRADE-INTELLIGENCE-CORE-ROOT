import json
import hashlib
from pathlib import Path


JOURNAL_FILE = Path(__file__).parent / "collapse_journal_log.json"


class ReplayViolation(Exception):
    pass


def hash_event(event_data: dict):
    # Remove event_hash before recomputing
    event_copy = dict(event_data)
    original_hash = event_copy.pop("event_hash")

    serialized = json.dumps(event_copy, sort_keys=True)
    computed_hash = hashlib.sha256(serialized.encode()).hexdigest()

    if computed_hash != original_hash:
        raise ReplayViolation("Hash mismatch detected during replay.")

    return computed_hash


def replay_journal():
    if not JOURNAL_FILE.exists():
        raise ReplayViolation("No journal found for replay.")

    with open(JOURNAL_FILE, "r") as f:
        journal = json.load(f)

    previous_hash = "GENESIS"
    state_sequence = []

    for event in journal:
        # Verify hash chain continuity
        if event["previous_hash"] != previous_hash:
            raise ReplayViolation("Hash chain broken.")

        computed_hash = hash_event(event)

        previous_hash = computed_hash
        state_sequence.append(event["target_state"])

    return state_sequence, previous_hash


if __name__ == "__main__":
    try:
        states, final_hash = replay_journal()
        print("Replay successful.")
        print("State sequence:", states)
        print("Final hash:", final_hash)
    except ReplayViolation as e:
        print("Replay failed:", e)
