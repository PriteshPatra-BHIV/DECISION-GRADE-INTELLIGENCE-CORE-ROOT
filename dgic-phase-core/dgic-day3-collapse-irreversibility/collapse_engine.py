import json
import hashlib
import uuid
from pathlib import Path
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from ambiguity_archive import AmbiguityArchive

MODULE_DIR = Path(__file__).parent
COLLAPSE_LEDGER_FILE = MODULE_DIR / "collapse_ledger.json"


class CollapseViolation(Exception):
    pass


class CollapseEngine:

    def __init__(self):
        self.previous_hash = self._get_last_hash()

    def _get_last_hash(self):
        if COLLAPSE_LEDGER_FILE.exists():
            with open(COLLAPSE_LEDGER_FILE, "r") as f:
                data = json.load(f)
                if data:
                    return data[-1]["event_hash"]
        return "GENESIS"

    def _hash_event(self, event_data):
        serialized = json.dumps(event_data, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def collapse(self, previous_state, evidence_reference):
        """
        Performs irreversible collapse:
        - Archives ambiguity (if applicable)
        - Logs collapse event
        - Hash-chains ledger entry
        """

        # Collapse only allowed from Ambiguous or Inferred
        if previous_state not in ["Ambiguous", "Inferred"]:
            raise CollapseViolation(
                f"Collapse not allowed from state: {previous_state}"
            )

        if not evidence_reference:
            raise CollapseViolation(
                "Evidence reference required for collapse."
            )

        # Archive ambiguity before collapse
        if previous_state == "Ambiguous":
            archive = AmbiguityArchive()
            archive.archive(
                previous_state=previous_state,
                context_reference=evidence_reference
            )

        event = {
            "collapse_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "previous_state": previous_state,
            "new_state": "Known",
            "evidence_reference": evidence_reference,
            "previous_hash": self.previous_hash,
        }

        event_hash = self._hash_event(event)
        event["event_hash"] = event_hash

        self._append_ledger(event)

        self.previous_hash = event_hash

        return event

    def _append_ledger(self, event):
        if COLLAPSE_LEDGER_FILE.exists():
            with open(COLLAPSE_LEDGER_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(event)

        with open(COLLAPSE_LEDGER_FILE, "w") as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    engine = CollapseEngine()

    try:
        collapse_event = engine.collapse(
            previous_state="Ambiguous",
            evidence_reference="Signal_#456"
        )
        print("Collapse successful:", collapse_event)
    except CollapseViolation as e:
        print("Blocked:", e)
