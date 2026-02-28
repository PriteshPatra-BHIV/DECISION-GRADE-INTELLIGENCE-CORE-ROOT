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


def test_missing_signals_block_inference():
    """
    Without signals, system must remain Unknown.
    """
    
    current_state = KnowledgeState.UNKNOWN
    
    # Attempt to infer without signal → must fail
    try:
        enforce_transition(
            current_state,
            KnowledgeState.INFERRED
        )
        assert False, "Should have blocked inference without signal"
    except TransitionViolation:
        pass  # Correctly blocked
    
    print("[PASS] Missing signals blocked inference")


def test_incomplete_data_prevents_promotion():
    """
    Partial data must not promote to Known.
    """
    
    current_state = KnowledgeState.INFERRED
    
    # Attempt promotion without new evidence
    try:
        enforce_transition(
            current_state,
            KnowledgeState.KNOWN,
            new_evidence=False
        )
        assert False, "Should have blocked promotion"
    except TransitionViolation:
        pass  # Correctly blocked
    
    print("[PASS] Incomplete data prevented promotion")


def test_signal_removal_degrades_state():
    """
    When signals are removed, certainty must degrade.
    """
    
    current_state = KnowledgeState.AMBIGUOUS
    
    # Signal removal → must allow degradation to Unknown
    enforce_transition(
        current_state,
        KnowledgeState.UNKNOWN
    )
    
    print("[PASS] Signal removal correctly degraded state")


if __name__ == "__main__":
    test_missing_signals_block_inference()
    test_incomplete_data_prevents_promotion()
    test_signal_removal_degrades_state()
    print("\n[PASS] All missing signal tests passed")
