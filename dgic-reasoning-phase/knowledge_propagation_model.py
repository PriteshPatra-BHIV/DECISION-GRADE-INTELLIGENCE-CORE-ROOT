"""Knowledge propagation model for DGIC reasoning layer."""

from typing import List
from multi_state_model import EpistemicState, EpistemicStateSet
from exceptions import ValidationError, PropagationError
from logger import get_logger


class KnowledgePropagationModel:
    """Simulates distributed knowledge sharing between reasoning nodes.
    Nodes exchange partial epistemic states and update confidence.
    Deterministic propagation only.
    """

    def __init__(self) -> None:
        get_logger().debug("KnowledgePropagationModel initialized")

    def propagate(self, node_states: List[EpistemicStateSet]) -> EpistemicStateSet:
        """Aggregate knowledge from multiple nodes.
        
        Args:
            node_states: List of EpistemicStateSet objects from different nodes
            
        Returns:
            Aggregated global state set
        """
        try:
            self._validate_inputs(node_states)
            
            aggregated_confidence = {}
            evidence_map = {}

            # Collect information from all nodes
            for node_idx, state_set in enumerate(node_states):
                for state in state_set.get_states():
                    key = state.epistemic_state

                    if key not in aggregated_confidence:
                        aggregated_confidence[key] = []
                        evidence_map[key] = state.evidence_set
                    else:
                        # Merge evidence sets deterministically
                        evidence_map[key] = sorted(
                            set(evidence_map[key] + state.evidence_set)
                        )

                    aggregated_confidence[key].append(state.confidence)

            # Compute deterministic average confidence
            global_state_set = EpistemicStateSet()

            for state_type, confidences in aggregated_confidence.items():
                avg_confidence = sum(confidences) / len(confidences)
                entropy = 1 - avg_confidence

                new_state = EpistemicState(
                    epistemic_state=state_type,
                    confidence=avg_confidence,
                    entropy=entropy,
                    evidence_set=evidence_map[state_type]
                )

                global_state_set.add_state(new_state)

            get_logger().info(
                f"Propagated knowledge from {len(node_states)} nodes, "
                f"aggregated {len(aggregated_confidence)} state types"
            )
            return global_state_set
        
        except ValidationError:
            raise
        except Exception as e:
            get_logger().error(f"Knowledge propagation failed: {e}")
            raise PropagationError(f"Failed to propagate knowledge: {e}")

    def _validate_inputs(self, node_states: List[EpistemicStateSet]) -> None:
        """Validate input parameters."""
        if not isinstance(node_states, list):
            raise ValidationError(f"Expected list, got {type(node_states)}")
        
        if len(node_states) == 0:
            raise ValidationError("node_states cannot be empty")
        
        for i, state_set in enumerate(node_states):
            if not isinstance(state_set, EpistemicStateSet):
                raise ValidationError(
                    f"node_states[{i}] must be EpistemicStateSet, got {type(state_set)}"
                )
