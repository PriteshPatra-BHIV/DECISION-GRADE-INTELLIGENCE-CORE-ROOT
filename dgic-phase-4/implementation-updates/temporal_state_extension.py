from datetime import datetime
from enum import Enum


class TemporalState(Enum):
    PRE_OBSERVATION = "Pre-Observation"
    OBSERVED = "Observed"
    COLLAPSED = "Collapsed"
    ARCHIVED = "Archived"


class TemporalViolation(Exception):
    pass


class TemporalStateController:

    def __init__(self):
        self.temporal_state = TemporalState.PRE_OBSERVATION
        self.last_event_timestamp = None

    def transition(self, new_state: TemporalState):
        now = datetime.utcnow()

        # Enforce forward-only time
        if self.last_event_timestamp and now <= self.last_event_timestamp:
            raise TemporalViolation("Temporal ordering violation.")

        allowed_transitions = {
            TemporalState.PRE_OBSERVATION: [TemporalState.OBSERVED],
            TemporalState.OBSERVED: [TemporalState.COLLAPSED, TemporalState.ARCHIVED],
            TemporalState.COLLAPSED: [TemporalState.ARCHIVED],
            TemporalState.ARCHIVED: [],
        }

        if new_state not in allowed_transitions[self.temporal_state]:
            raise TemporalViolation(
                f"Illegal temporal transition: "
                f"{self.temporal_state.value} → {new_state.value}"
            )

        self.temporal_state = new_state
        self.last_event_timestamp = now

        return {
            "new_temporal_state": self.temporal_state.value,
            "event_timestamp": now.isoformat(),
        }


if __name__ == "__main__":
    controller = TemporalStateController()

    try:
        controller.transition(TemporalState.OBSERVED)
        controller.transition(TemporalState.COLLAPSED)
        controller.transition(TemporalState.ARCHIVED)
        print("Temporal transitions successful.")
    except TemporalViolation as e:
        print("Blocked:", e)
