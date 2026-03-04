from dataclasses import dataclass


@dataclass(frozen=True)
class EpistemicSnapshot:
    epistemic_state: str
    confidence: float
    contradiction_flag: bool
    evidence_hash: str
    collapse_flag: bool
    entropy_score: float