import json
import uuid
from datetime import datetime
from pathlib import Path


JOURNAL_FILE = Path("epistemic_journal_log.json")


class JournalViolation(Exception):
    pass


def log_collapse_event(
    previous_state: str,
    target_state: str,
    evidence_reference: str,
    justification: str,
    actor: str = "system",
):
    """
    Append-only collapse logging.
    """

    if not evidence_reference or not justification:
        raise JournalViolation("Collapse requires evidence and justification.")

    entry = {
        "transition_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "previous_state": previous_state,
        "target_state": target_state,
        "evidence_reference": evidence_reference,
        "justification": justification,
        "actor": actor,
    }

    # Ensure append-only behavior
    if JOURNAL_FILE.exists():
        with open(JOURNAL_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(JOURNAL_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return entry


if __name__ == "__main__":
    # Example test log
    try:
        event = log_collapse_event(
            previous_state="Ambiguous",
            target_state="Known",
            evidence_reference="Signal_#123",
            justification="New verified signal resolved conflict",
        )
        print("Logged:", event["transition_id"])
    except JournalViolation as e:
        print("Blocked:", e)
