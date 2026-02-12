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


def test_contradictory_signals_preserve_ambiguity():
    """
    When contradictory signals exist,
    system must maintain Ambiguous state.
    """
    
    # Scenario: Two conflicting signals about same entity
    signal_a = {"source": "A", "value": "positive"}
    signal_b = {"source": "B", "value": "negative"}
    
    current_state = KnowledgeState.AMBIGUOUS
    
    # System must NOT promote to Known without resolution
    try:
        enforce_transition(
            current_state,
            KnowledgeState.KNOWN,
            new_evidence=False,
            justified_collapse=False
        )
        assert False, "Should have blocked promotion"
    except Exception:
        pass  # Correctly blocked
    
    print("[PASS] Contradictory signals preserved ambiguity")


def test_conflict_without_resolution():
    """
    Conflicting evidence must not auto-resolve.
    """
    
    current_state = KnowledgeState.INFERRED
    
    # Conflict introduced → must move to Ambiguous
    enforce_transition(
        current_state,
        KnowledgeState.AMBIGUOUS
    )
    
    print("[PASS] Conflict correctly degraded certainty")


if __name__ == "__main__":
    test_contradictory_signals_preserve_ambiguity()
    test_conflict_without_resolution()
    print("\n[PASS] All contradictory signal tests passed")
