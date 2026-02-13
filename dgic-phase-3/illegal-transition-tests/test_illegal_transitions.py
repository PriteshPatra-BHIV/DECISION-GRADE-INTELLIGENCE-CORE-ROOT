from state_engine import DeterministicStateEngine, StateViolation


def test_unknown_to_known_blocked():
    engine = DeterministicStateEngine()

    try:
        engine.transition("Known")
        print("FAIL: Unknown → Known should be blocked.")
    except StateViolation:
        print("PASS: Unknown → Known blocked.")


def test_inferred_to_known_without_evidence_blocked():
    engine = DeterministicStateEngine()

    engine.transition("Ambiguous")  # Unknown → Ambiguous
    engine.transition("Unknown")    # Ambiguous → Unknown
    engine.transition("Ambiguous")  # Unknown → Ambiguous
    engine.transition("Inferred") if False else None
    # Instead, simulate Inferred properly
    engine.current_state = "Inferred"

    try:
        engine.transition("Known", new_evidence=False)
        print("FAIL: Inferred → Known without evidence should be blocked.")
    except StateViolation:
        print("PASS: Inferred → Known without evidence blocked.")


def test_ambiguous_to_known_requires_collapse():
    engine = DeterministicStateEngine()

    engine.transition("Ambiguous")

    try:
        engine.transition("Known", new_evidence=True, justified_collapse=False)
        print("FAIL: Ambiguous → Known without justified collapse should be blocked.")
    except StateViolation:
        print("PASS: Ambiguous → Known without justified collapse blocked.")


if __name__ == "__main__":
    test_unknown_to_known_blocked()
    test_inferred_to_known_without_evidence_blocked()
    test_ambiguous_to_known_requires_collapse()
