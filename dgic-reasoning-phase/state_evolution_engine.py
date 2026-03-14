"""State evolution engine for DGIC reasoning layer."""

from typing import List, Dict
from multi_state_model import EpistemicState, EpistemicStateSet
from exceptions import ValidationError, EvolutionError
from config import get_config
from logger import get_logger


class StateEvolutionEngine:
    """Evolves epistemic hypotheses when new evidence arrives.
    Deterministic and replay-safe.
    """

    def __init__(self) -> None:
        get_logger().debug("StateEvolutionEngine initialized")

    def evolve_states(
        self,
        state_set: EpistemicStateSet,
        new_evidence: Dict
    ) -> EpistemicStateSet:
        """Apply deterministic evolution rules to all states."""
        try:
            self._validate_inputs(state_set, new_evidence)
            
            evolved_set = EpistemicStateSet()
            config = get_config()

            for state in state_set.get_states():
                relation = self._evaluate_relation(
                    state.epistemic_state,
                    new_evidence
                )

                new_confidence, new_entropy = self._update_metrics(
                    state.confidence,
                    state.entropy,
                    relation,
                    config
                )

                updated_evidence = state.evidence_set + [new_evidence["signal_id"]]

                evolved_state = EpistemicState(
                    epistemic_state=state.epistemic_state,
                    confidence=new_confidence,
                    entropy=new_entropy,
                    evidence_set=updated_evidence
                )

                evolved_set.add_state(evolved_state)

            get_logger().info(f"Evolved {state_set.size()} states with evidence {new_evidence['signal_id']}")
            return evolved_set
        
        except ValidationError:
            raise
        except Exception as e:
            get_logger().error(f"State evolution failed: {e}")
            raise EvolutionError(f"Failed to evolve states: {e}")

    def _validate_inputs(self, state_set: EpistemicStateSet, evidence: Dict) -> None:
        """Validate input parameters."""
        if not isinstance(state_set, EpistemicStateSet):
            raise ValidationError(f"Expected EpistemicStateSet, got {type(state_set)}")
        
        if not isinstance(evidence, dict):
            raise ValidationError(f"Expected dict for evidence, got {type(evidence)}")
        
        if "signal_id" not in evidence:
            raise ValidationError("evidence must contain 'signal_id'")
        
        if "type" not in evidence:
            raise ValidationError("evidence must contain 'type'")
        
        if not isinstance(evidence["signal_id"], str):
            raise ValidationError("signal_id must be string")
        
        if not isinstance(evidence["type"], str):
            raise ValidationError("evidence type must be string")

    def _evaluate_relation(self, state_type: str, evidence: Dict) -> str:
        """Determine relation between evidence and hypothesis."""
        evidence_type = evidence.get("type", "")
        
        if evidence_type == state_type:
            return "support"
        
        if evidence_type == "CONTRADICTION":
            return "contradict"
        
        return "neutral"

    def _update_metrics(
        self,
        confidence: float,
        entropy: float,
        relation: str,
        config
    ) -> tuple:
        """Deterministically update confidence and entropy."""
        if relation == "support":
            confidence += config.support_confidence_boost
            entropy -= config.support_entropy_reduction
        
        elif relation == "contradict":
            confidence -= config.contradict_confidence_penalty
            entropy += config.contradict_entropy_increase
        
        else:
            entropy += config.neutral_entropy_increase

        confidence = max(config.min_confidence, min(config.max_confidence, confidence))
        entropy = max(config.min_entropy, min(config.max_entropy, entropy))

        return confidence, entropy
