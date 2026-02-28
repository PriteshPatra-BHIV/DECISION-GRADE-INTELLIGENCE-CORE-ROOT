import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from collapse_engine import CollapseEngine, CollapseViolation
import hashlib


MODULE_DIR = Path(__file__).parent.parent
LEDGER_FILE = MODULE_DIR / "collapse_ledger.json"


class ReplayViolation(Exception):
    pass


def verify_hash_chain():
    if not LEDGER_FILE.exists():
        raise ReplayViolation("Ledger not found.")

    with open(LEDGER_FILE, "r") as f:
        ledger = json.load(f)

    previous_hash = "GENESIS"

    for entry in ledger:
        stored_hash = entry["event_hash"]
        event_copy = dict(entry)
        event_copy.pop("event_hash")

        serialized = json.dumps(event_copy, sort_keys=True)
        computed_hash = hashlib.sha256(serialized.encode()).hexdigest()

        if computed_hash != stored_hash:
            raise ReplayViolation("Hash mismatch detected.")

        if entry["previous_hash"] != previous_hash:
            raise ReplayViolation("Hash chain broken.")

        previous_hash = stored_hash


def test_mutation_attack():
    engine = CollapseEngine()
    engine.collapse("Ambiguous", "Signal_1")

    assert LEDGER_FILE.exists(), "Ledger not created"

    # Tamper with ledger manually
    with open(LEDGER_FILE, "r") as f:
        ledger = json.load(f)

    ledger[0]["new_state"] = "Unknown"  # Corruption attempt

    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

    # Verify mutation is detected
    try:
        verify_hash_chain()
        assert False, "Mutation not detected"
    except ReplayViolation:
        pass  # Expected - mutation detected


if __name__ == "__main__":
    test_mutation_attack()
