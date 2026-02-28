import json
import hashlib
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from collapse_engine import CollapseEngine
import os


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
            raise ReplayViolation("Hash mismatch.")

        if entry["previous_hash"] != previous_hash:
            raise ReplayViolation("Hash chain broken.")

        previous_hash = stored_hash

    return previous_hash


def test_multiple_collapses():
    # Clean up ledger before test
    if LEDGER_FILE.exists():
        os.remove(LEDGER_FILE)
    
    engine = CollapseEngine()

    # Perform multiple collapses
    engine.collapse("Ambiguous", "Signal_A")
    engine.collapse("Ambiguous", "Signal_B")
    engine.collapse("Inferred", "Signal_C")

    final_hash = verify_hash_chain()
    assert final_hash is not None, "Hash chain verification failed"


if __name__ == "__main__":
    test_multiple_collapses()
