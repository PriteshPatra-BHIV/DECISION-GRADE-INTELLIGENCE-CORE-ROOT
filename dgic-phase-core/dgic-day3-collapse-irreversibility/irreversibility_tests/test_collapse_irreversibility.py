import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from collapse_engine import CollapseEngine, CollapseViolation
import json


MODULE_DIR = Path(__file__).parent.parent
LEDGER_FILE = MODULE_DIR / "collapse_ledger.json"


def test_illegal_collapse_from_known():
    engine = CollapseEngine()

    try:
        engine.collapse(previous_state="Known", evidence_reference="X")
        assert False, "Collapse from Known should be blocked"
    except CollapseViolation:
        pass  # Expected


def test_evidence_required():
    engine = CollapseEngine()

    try:
        engine.collapse(previous_state="Ambiguous", evidence_reference=None)
        assert False, "Collapse without evidence should be blocked"
    except CollapseViolation:
        pass  # Expected


def test_append_only_behavior():
    engine = CollapseEngine()

    engine.collapse(previous_state="Ambiguous", evidence_reference="Signal_1")

    assert LEDGER_FILE.exists(), "Ledger file not created"
    
    with open(LEDGER_FILE, "r") as f:
        ledger = json.load(f)

    assert len(ledger) >= 1, "Ledger entry missing"


if __name__ == "__main__":
    test_illegal_collapse_from_known()
    test_evidence_required()
    test_append_only_behavior()
