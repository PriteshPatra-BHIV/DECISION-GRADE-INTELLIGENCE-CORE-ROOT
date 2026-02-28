import json
import hashlib
import uuid
from pathlib import Path
import os

# Get the directory where this module is located
MODULE_DIR = Path(__file__).parent
TRANSITION_MATRIX_FILE = MODULE_DIR / "transition-matrix.json"
JOURNAL_FILE = MODULE_DIR / "state_journal.json"


class StateViolation(Exception):
    pass


class DeterministicStateEngine:

    def __init__(self):
        self.current_state = "Unknown"
        self.previous_hash = "GENESIS"
        self.transition_matrix = self._load_matrix()

    def _load_matrix(self):
        with open(TRANSITION_MATRIX_FILE, "r") as f:
            return json.load(f)

    def _hash_event(self, event_data):
        serialized = json.dumps(event_data, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def transition(self, target_state, new_evidence=False):
        rules = self.transition_matrix.get(self.current_state)

        if not rules:
            raise StateViolation("Invalid current state.")

        # Check allowed transitions
        if target_state not in rules["allowed"]:
            raise StateViolation(
                f"Illegal transition: {self.current_state} → {target_state}"
            )

        # Evidence enforcement
        if "requires_evidence" in rules:
            if target_state in rules["requires_evidence"] and not new_evidence:
                raise StateViolation("Transition requires new evidence.")

        event = {
            "transition_id": str(uuid.uuid4()),
            "previous_state": self.current_state,
            "target_state": target_state,
            "new_evidence": new_evidence,
            "previous_hash": self.previous_hash,
        }

        event_hash = self._hash_event(event)
        event["event_hash"] = event_hash

        self._append_journal(event)

        self.previous_hash = event_hash
        self.current_state = target_state

        return event

    def _append_journal(self, event):
        if JOURNAL_FILE.exists():
            with open(JOURNAL_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(event)

        with open(JOURNAL_FILE, "w") as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    engine = DeterministicStateEngine()

    try:
        engine.transition("Ambiguous")
        engine.transition("Inferred")
        engine.transition("Known", new_evidence=True)
        print("Transitions successful.")
    except StateViolation as e:
        print("Blocked:", e)
