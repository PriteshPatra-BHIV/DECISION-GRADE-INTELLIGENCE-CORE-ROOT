import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "day-1"))
from integration_harness import DGICIntegrationHarness


class EnforcementAdapter:
    """
    Simulates Rajaryan's bounded risk scoring engine.
    """

    def __init__(self, integration_harness: DGICIntegrationHarness):
        self._harness = integration_harness

    def compute_risk_score(self) -> float:
        """
        Deterministic bounded risk scoring.
        No mutation allowed.
        """

        snapshot = self._harness.generate_snapshot()

        # Risk model rules (bounded, deterministic)
        if snapshot.contradiction_flag:
            return 0.9

        if snapshot.epistemic_state == "CERTAIN":
            return 0.2

        if snapshot.epistemic_state == "AMBIGUOUS":
            return 0.5

        return 0.7