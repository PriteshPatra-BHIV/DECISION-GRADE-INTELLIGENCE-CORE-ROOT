"""State interference model for DGIC reasoning layer."""

from multi_state_model import EpistemicState, EpistemicStateSet
from exceptions import ValidationError, InterferenceError
from config import get_config
from logger import get_logger


class StateInterferenceModel:
    """Handles interaction between epistemic hypotheses.
    Compatible states reinforce each other.
    Conflicting states weaken each other.
    Deterministic behavior only.
    """

    def __init__(self) -> None:
        get_logger().debug("StateInterferenceModel initialized")

    def apply_interference(self, state_set: EpistemicStateSet) -> EpistemicStateSet:
        """Apply deterministic interference between states."""
        try:
            if not isinstance(state_set, EpistemicStateSet):
                raise ValidationError(f"Expected EpistemicStateSet, got {type(state_set)}")
            
            states = state_set.get_states()
            new_state_set = EpistemicStateSet()
            config = get_config()

            for i, state_a in enumerate(states):
                confidence_adjustment = 0.0
                entropy_adjustment = 0.0

                for j, state_b in enumerate(states):
                    if i == j:
                        continue

                    relation = self._relation(state_a, state_b)

                    if relation == "compatible":
                        confidence_adjustment += config.compatible_confidence_boost
                        entropy_adjustment -= config.compatible_entropy_reduction

                    elif relation == "conflict":
                        if state_b.confidence > state_a.confidence:
                            confidence_adjustment -= config.conflict_confidence_penalty
                            entropy_adjustment += config.conflict_entropy_increase

                new_confidence = self._clamp(
                    state_a.confidence + confidence_adjustment,
                    config
                )
                new_entropy = self._clamp(
                    state_a.entropy + entropy_adjustment,
                    config
                )

                updated_state = EpistemicState(
                    epistemic_state=state_a.epistemic_state,
                    confidence=new_confidence,
                    entropy=new_entropy,
                    evidence_set=state_a.evidence_set
                )

                new_state_set.add_state(updated_state)

            get_logger().info(f"Applied interference to {state_set.size()} states")
            return new_state_set
        
        except ValidationError:
            raise
        except Exception as e:
            get_logger().error(f"Interference calculation failed: {e}")
            raise InterferenceError(f"Failed to apply interference: {e}")

    def _relation(self, state_a: EpistemicState, state_b: EpistemicState) -> str:
        """Determine relationship between two states."""
        if state_a.epistemic_state == state_b.epistemic_state:
            return "compatible"
        return "conflict"

    def _clamp(self, value: float, config) -> float:
        """Clamp value to valid range."""
        return max(config.min_confidence, min(config.max_confidence, value))
