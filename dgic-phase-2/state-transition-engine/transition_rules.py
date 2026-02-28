from enum import Enum


class KnowledgeState(Enum):
    KNOWN = "Known"
    INFERRED = "Inferred"
    AMBIGUOUS = "Ambiguous"
    UNKNOWN = "Unknown"


# Structural transition map
ALLOWED_TRANSITIONS = {
    KnowledgeState.KNOWN: [
        KnowledgeState.INFERRED,
    ],
    KnowledgeState.INFERRED: [
        KnowledgeState.AMBIGUOUS,
        KnowledgeState.KNOWN,
    ],
    KnowledgeState.AMBIGUOUS: [
        KnowledgeState.UNKNOWN,
        KnowledgeState.KNOWN,
    ],
    KnowledgeState.UNKNOWN: [
        KnowledgeState.AMBIGUOUS,
    ],
}


class TransitionViolation(Exception):
    pass


def enforce_transition(
    current_state: KnowledgeState,
    target_state: KnowledgeState,
    *,
    new_evidence: bool = False,
    justified_collapse: bool = False,
):
    """
    Enforces epistemic state transitions.

    Raises TransitionViolation if transition is illegal.
    """

    # Structural check
    if target_state not in ALLOWED_TRANSITIONS.get(current_state, []):
        raise TransitionViolation(
            f"Illegal structural transition: {current_state.value} → {target_state.value}"
        )

    # Promotion safeguards
    if current_state == KnowledgeState.INFERRED and target_state == KnowledgeState.KNOWN:
        if not new_evidence:
            raise TransitionViolation(
                "Inferred → Known requires new evidence."
            )

    if current_state == KnowledgeState.AMBIGUOUS and target_state == KnowledgeState.KNOWN:
        if not (new_evidence and justified_collapse):
            raise TransitionViolation(
                "Ambiguous → Known requires new evidence AND justified collapse."
            )

    return True


if __name__ == "__main__":
    # Example enforcement test
    try:
        enforce_transition(
            KnowledgeState.AMBIGUOUS,
            KnowledgeState.KNOWN,
            new_evidence=False,
            justified_collapse=False,
        )
    except TransitionViolation as e:
        print("Blocked:", e)
