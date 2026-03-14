"""Collapse policy engine for DGIC reasoning layer."""

from typing import Optional
from multi_state_model import EpistemicState, EpistemicStateSet
from exceptions import ValidationError, CollapseError
from config import get_config
from logger import get_logger


class CollapsePolicyEngine:
    """Determines when epistemic uncertainty should collapse
    into a single dominant hypothesis.
    """

    def __init__(self) -> None:
        get_logger().debug("CollapsePolicyEngine initialized")

    def evaluate_collapse(self, state_set: EpistemicStateSet) -> Optional[EpistemicState]:
        """Evaluate if state set should collapse to single hypothesis."""
        try:
            if not isinstance(state_set, EpistemicStateSet):
                raise ValidationError(f"Expected EpistemicStateSet, got {type(state_set)}")
            
            states = state_set.get_states()

            if len(states) == 0:
                get_logger().debug("Empty state set, no collapse")
                return None

            config = get_config()
            states = sorted(states, key=lambda s: s.confidence, reverse=True)
            top_state = states[0]

            # Rule 1: confidence threshold
            if top_state.confidence >= config.confidence_threshold:
                get_logger().info(
                    f"Collapse triggered by confidence threshold: "
                    f"{top_state.epistemic_state} ({top_state.confidence})"
                )
                return top_state

            # Rule 2: entropy floor
            if top_state.entropy <= config.entropy_floor:
                get_logger().info(
                    f"Collapse triggered by entropy floor: "
                    f"{top_state.epistemic_state} (entropy={top_state.entropy})"
                )
                return top_state

            # Rule 3: dominance gap
            if len(states) > 1:
                second_state = states[1]
                gap = top_state.confidence - second_state.confidence

                if gap >= config.dominance_gap:
                    get_logger().info(
                        f"Collapse triggered by dominance gap: "
                        f"{top_state.epistemic_state} (gap={gap})"
                    )
                    return top_state

            get_logger().debug("No collapse conditions met, ambiguity preserved")
            return None
        
        except ValidationError:
            raise
        except Exception as e:
            get_logger().error(f"Collapse evaluation failed: {e}")
            raise CollapseError(f"Failed to evaluate collapse: {e}")
