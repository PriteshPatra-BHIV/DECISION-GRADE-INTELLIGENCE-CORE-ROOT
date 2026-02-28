import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from collapse_engine import CollapseEngine
from ambiguity_archive import AmbiguityArchive


MODULE_DIR = Path(__file__).parent.parent
ARCHIVE_FILE = MODULE_DIR / "ambiguity_archive.json"
LEDGER_FILE = MODULE_DIR / "collapse_ledger.json"


def test_ambiguity_persistence():
    engine = CollapseEngine()

    # Perform collapse from Ambiguous
    engine.collapse("Ambiguous", "Signal_X")

    assert ARCHIVE_FILE.exists(), "Ambiguity archive not created"

    with open(ARCHIVE_FILE, "r") as f:
        archive = json.load(f)

    assert len(archive) > 0, "Ambiguity not archived"
    assert LEDGER_FILE.exists(), "Collapse ledger not created"


if __name__ == "__main__":
    test_ambiguity_persistence()
