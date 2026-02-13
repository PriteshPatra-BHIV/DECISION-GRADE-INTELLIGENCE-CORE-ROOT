import json
import hashlib
import uuid
from datetime import datetime
from pathlib import Path


TRANSITION_MATRIX_FILE = Path("transition-matrix.json")
JOURNAL_FILE = Path("collapse_journal_log.json")


class StateViolation(Exception):
    pass


class DeterministicStateEngine:

    def __init__(self):
        self.current_state = "Unknown"
        self.transition_matrix = self._load_matrix()
        self.previous_hash = "GENESIS"

    def _load_matrix(self):
        with open(TRANSITION_MATRIX_FILE, "r") as f:
            return json.load(f)

    def _hash_event(self, event_data: dict):
        serialized = json.dumps(event_data, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def transition(
        self,
        target_state: str,
        new_evidence: bool = False,
        justified_collapse: bool = False,
    ):
        rules = self.transition_matrix[self.current_state]

        # Structural validation
        if target_state not in rules["allowed"]:
            raise StateViolation(
                f"Illegal transition: {self.current_state} → {target_state}"
            )

        # Evidence enforcement
        if target_state in rules["requires_evidence"] and not new_evidence:
            raise StateViolation("Transition requires new evidence.")

        # Collapse enforcement
        if target_state in rules["requires_collapse"] and not justified_collapse:
            raise StateViolation("Transition requires justified collapse.")

        # Create event
        event = {
            "transition_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "previous_state": self.current_state,
            "target_state": target_state,
            "new_evidence": new_evidence,
            "justified_collapse": justified_collapse,
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
        engine.transition("Known", new_evidence=True, justified_collapse=True)
        print("Transitions successful.")
    except StateViolation as e:
        print("Blocked:", e)
