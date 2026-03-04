import copy
from snapshot_model import EpistemicSnapshot
from serialization_discipline import hash_evidence, deterministic_json


class DGICIntegrationHarness:

    def __init__(self, dgic_core):
        self._core = dgic_core  # private reference

    def generate_snapshot(self) -> EpistemicSnapshot:
        """
        Extract immutable snapshot from DGIC core.
        """

        state = copy.deepcopy(self._core.get_state())

        return EpistemicSnapshot(
            epistemic_state=state["epistemic_state"],
            confidence=state["confidence"],
            contradiction_flag=state["contradiction_flag"],
            evidence_hash=hash_evidence(state["evidence"]),
            collapse_flag=state["collapse_flag"],
            entropy_score=state["entropy_score"],
        )

    def serialize_snapshot(self) -> str:
        snapshot = self.generate_snapshot()
        return deterministic_json(snapshot.__dict__)

    def deterministic_replay_check(self, iterations=1000) -> bool:
        baseline = self.serialize_snapshot()

        for _ in range(iterations):
            if self.serialize_snapshot() != baseline:
                return False

        return True