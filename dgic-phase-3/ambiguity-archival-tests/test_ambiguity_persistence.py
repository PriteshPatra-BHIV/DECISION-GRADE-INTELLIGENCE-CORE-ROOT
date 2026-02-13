from state_engine import DeterministicStateEngine, StateViolation
from replay_harness import replay_journal


def test_ambiguity_requires_evidence():
    engine = DeterministicStateEngine()

    # Move to Ambiguous first
    engine.transition("Ambiguous")

    try:
        # Attempt illegal collapse without evidence
        engine.transition("Known", new_evidence=False, justified_collapse=False)
        print("FAIL: Ambiguity collapsed without evidence.")
    except StateViolation:
        print("PASS: Ambiguity collapse blocked without evidence.")


def test_ambiguity_archived_on_valid_collapse():
    engine = DeterministicStateEngine()

    engine.transition("Ambiguous")

    # Proper collapse
    engine.transition("Known", new_evidence=True, justified_collapse=True)

    states, final_hash = replay_journal()

    if "Ambiguous" not in states:
        print("FAIL: Ambiguity not preserved in replay history.")
    else:
        print("PASS: Ambiguity preserved in replay history.")


if __name__ == "__main__":
    test_ambiguity_requires_evidence()
    test_ambiguity_archived_on_valid_collapse()
