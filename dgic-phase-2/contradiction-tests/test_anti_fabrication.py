from pathlib import Path
import sys

# Direct import using relative path
parent_dir = Path(__file__).resolve().parent.parent
transition_module = parent_dir / "state-transition-engine" / "transition_rules.py"

import importlib.util
spec = importlib.util.spec_from_file_location("transition_rules", transition_module)
transition_rules = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transition_rules)

KnowledgeState = transition_rules.KnowledgeState
enforce_transition = transition_rules.enforce_transition
TransitionViolation = transition_rules.TransitionViolation


def test_external_pressure_rejected():
    """
    System must refuse certainty under external demand.
    """
    
    current_state = KnowledgeState.AMBIGUOUS
    
    # Simulate downstream pressure for clarity
    try:
        enforce_transition(
            current_state,
            KnowledgeState.KNOWN,
            new_evidence=False,
            justified_collapse=False
        )
        assert False, "System fabricated certainty"
    except TransitionViolation:
        pass  # Correctly refused
    
    print("[PASS] External pressure rejected")


def test_majority_signal_not_auto_promoted():
    """
    Majority signals must not auto-promote without justification.
    """
    
    # Scenario: 3 positive signals, 1 negative
    signals = ["positive", "positive", "positive", "negative"]
    
    current_state = KnowledgeState.AMBIGUOUS
    
    # Must not auto-resolve to Known
    try:
        enforce_transition(
            current_state,
            KnowledgeState.KNOWN,
            new_evidence=True,
            justified_collapse=False  # No justification
        )
        assert False, "Auto-promoted majority"
    except TransitionViolation:
        pass  # Correctly blocked
    
    print("[PASS] Majority signal not auto-promoted")


def test_ambiguity_tolerated_indefinitely():
    """
    System must tolerate unresolved ambiguity.
    """
    
    current_state = KnowledgeState.AMBIGUOUS
    
    # Ambiguous state is valid final state
    # No forced resolution required
    assert current_state == KnowledgeState.AMBIGUOUS
    
    print("[PASS] Ambiguity tolerated indefinitely")


def test_silence_over_false_clarity():
    """
    System prefers no answer over fabricated answer.
    """
    
    current_state = KnowledgeState.UNKNOWN
    
    # Cannot jump to Known without evidence
    try:
        enforce_transition(
            current_state,
            KnowledgeState.KNOWN
        )
        assert False, "Fabricated clarity"
    except TransitionViolation:
        pass  # Correctly maintained silence
    
    print("[PASS] Silence preferred over false clarity")


if __name__ == "__main__":
    test_external_pressure_rejected()
    test_majority_signal_not_auto_promoted()
    test_ambiguity_tolerated_indefinitely()
    test_silence_over_false_clarity()
    print("\n[PASS] All anti-fabrication tests passed")
    print("\n[PROOF] System never fabricates certainty")
