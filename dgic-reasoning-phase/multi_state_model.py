"""Multi-state representation for DGIC reasoning layer."""

from dataclasses import dataclass
from typing import List, Dict
import hashlib
from exceptions import ValidationError, StateError
from config import get_config
from logger import get_logger


@dataclass(frozen=True)
class EpistemicState:
    """Represents a single hypothesis inside the DGIC reasoning space.
    Immutable to preserve deterministic replay.
    """

    epistemic_state: str
    confidence: float
    entropy: float
    evidence_set: List[str]

    def __post_init__(self) -> None:
        """Validate state after initialization."""
        config = get_config()
        
        if not isinstance(self.epistemic_state, str) or not self.epistemic_state.strip():
            raise ValidationError("epistemic_state must be non-empty string")
        
        if not isinstance(self.confidence, (int, float)):
            raise ValidationError(f"confidence must be numeric, got {type(self.confidence)}")
        
        if not isinstance(self.entropy, (int, float)):
            raise ValidationError(f"entropy must be numeric, got {type(self.entropy)}")
        
        if not (config.min_confidence <= self.confidence <= config.max_confidence):
            raise ValidationError(
                f"confidence must be [{config.min_confidence},{config.max_confidence}], "
                f"got {self.confidence}"
            )
        
        if not (config.min_entropy <= self.entropy <= config.max_entropy):
            raise ValidationError(
                f"entropy must be [{config.min_entropy},{config.max_entropy}], "
                f"got {self.entropy}"
            )
        
        if not isinstance(self.evidence_set, list):
            raise ValidationError(f"evidence_set must be list, got {type(self.evidence_set)}")
        
        if not all(isinstance(e, str) for e in self.evidence_set):
            raise ValidationError("all evidence items must be strings")

    def evidence_hash(self) -> str:
        """Create deterministic hash of evidence set."""
        try:
            evidence_string = "|".join(sorted(self.evidence_set))
            return hashlib.sha256(evidence_string.encode()).hexdigest()
        except Exception as e:
            get_logger().error(f"Failed to compute evidence hash: {e}")
            raise StateError(f"Evidence hash computation failed: {e}")

    def to_dict(self) -> Dict:
        """Convert state to dictionary."""
        return {
            "epistemic_state": self.epistemic_state,
            "confidence": self.confidence,
            "entropy": self.entropy,
            "evidence_hash": self.evidence_hash(),
        }


class EpistemicStateSet:
    """Container for multiple epistemic hypotheses."""

    def __init__(self) -> None:
        self._states: List[EpistemicState] = []
        get_logger().debug("EpistemicStateSet initialized")

    def add_state(self, state: EpistemicState) -> None:
        """Add a hypothesis to the state set."""
        if not isinstance(state, EpistemicState):
            raise ValidationError(f"Expected EpistemicState, got {type(state)}")
        self._states.append(state)
        get_logger().debug(f"Added state: {state.epistemic_state}")

    def get_states(self) -> List[EpistemicState]:
        """Return states in deterministic order."""
        return sorted(
            self._states,
            key=lambda s: (s.epistemic_state, s.confidence)
        )

    def size(self) -> int:
        """Get number of states."""
        return len(self._states)

    def to_list(self) -> List[Dict]:
        """Convert states to serializable structure."""
        try:
            return [state.to_dict() for state in self.get_states()]
        except Exception as e:
            get_logger().error(f"Failed to convert state set to list: {e}")
            raise StateError(f"State set serialization failed: {e}")
