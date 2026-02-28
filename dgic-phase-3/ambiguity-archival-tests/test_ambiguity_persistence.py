import sys
from pathlib import Path
import os
sys.path.insert(0, str(Path(__file__).parent.parent))

from state_engine import DeterministicStateEngine, StateViolation, JOURNAL_FILE
from replay_harness import replay_journal


def test_ambiguity_requires_evidence():
    # Clean journal before test
    if JOURNAL_FILE.exists():
        os.remove(JOURNAL_FILE)
    
    engine = DeterministicStateEngine()

    # Move to Ambiguous first
    engine.transition("Ambiguous")

    try:
        # Attempt illegal collapse without evidence
        engine.transition("Known", new_evidence=False, justified_collapse=False)
        assert False, "Ambiguity collapsed without evidence."
    except StateViolation:
        pass  # Expected


def test_ambiguity_archived_on_valid_collapse():
    # Clean journal before test
    if JOURNAL_FILE.exists():
        os.remove(JOURNAL_FILE)
    
    engine = DeterministicStateEngine()

    engine.transition("Ambiguous")

    # Proper collapse
    engine.transition("Known", new_evidence=True, justified_collapse=True)

    states, final_hash = replay_journal()

    assert "Ambiguous" in states, "Ambiguity not preserved in replay history."


if __name__ == "__main__":
    test_ambiguity_requires_evidence()
    test_ambiguity_archived_on_valid_collapse()
