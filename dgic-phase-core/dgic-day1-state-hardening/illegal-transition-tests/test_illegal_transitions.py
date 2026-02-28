from state_engine import DeterministicStateEngine, StateViolation


def test_unknown_to_known_blocked():
    engine = DeterministicStateEngine()

    try:
        engine.transition("Known")
        print("FAIL: Unknown → Known should be blocked.")
    except StateViolation:
        print("PASS: Unknown → Known blocked.")


def test_unknown_to_inferred_blocked():
    engine = DeterministicStateEngine()

    try:
        engine.transition("Inferred")
        print("FAIL: Unknown → Inferred should be blocked.")
    except StateViolation:
        print("PASS: Unknown → Inferred blocked.")


def test_known_requires_evidence():
    engine = DeterministicStateEngine()

    engine.transition("Ambiguous")
    engine.transition("Inferred")

    try:
        engine.transition("Known", new_evidence=False)
        print("FAIL: Inferred → Known without evidence should be blocked.")
    except StateViolation:
        print("PASS: Evidence requirement enforced.")


if __name__ == "__main__":
    test_unknown_to_known_blocked()
    test_unknown_to_inferred_blocked()
    test_known_requires_evidence()
