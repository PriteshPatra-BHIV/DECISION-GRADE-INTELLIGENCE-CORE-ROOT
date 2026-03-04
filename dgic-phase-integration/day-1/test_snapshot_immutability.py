from snapshot_model import EpistemicSnapshot
import pytest


def test_snapshot_is_immutable():
    snapshot = EpistemicSnapshot(
        epistemic_state="AMBIGUOUS",
        confidence=0.5,
        contradiction_flag=False,
        evidence_hash="abc123",
        collapse_flag=False,
        entropy_score=0.4,
    )

    with pytest.raises(Exception):
        snapshot.confidence = 1.0