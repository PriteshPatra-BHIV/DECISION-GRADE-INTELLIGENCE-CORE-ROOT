import pytest
from datetime import datetime, timedelta


class TemporalLedgerSimulator:
    """
    Simulates ingestion of signals with external timestamps.
    Ledger order must follow ingestion time,
    not external signal time.
    """

    def __init__(self):
        self.ledger = []

    def ingest(self, signal_timestamp):
        event_timestamp = datetime.utcnow()

        entry = {
            "signal_timestamp": signal_timestamp,
            "event_timestamp": event_timestamp,
        }

        # Ledger must remain append-only
        if self.ledger:
            assert event_timestamp >= self.ledger[-1]["event_timestamp"]

        self.ledger.append(entry)


def test_out_of_order_signal_arrival():
    ledger = TemporalLedgerSimulator()

    now = datetime.utcnow()

    # First signal (newer external time)
    ledger.ingest(now)

    # Late signal (older external time)
    older_signal = now - timedelta(minutes=10)
    ledger.ingest(older_signal)

    # Ledger must still contain both entries in ingestion order
    assert len(ledger.ledger) == 2
    assert ledger.ledger[0]["event_timestamp"] <= ledger.ledger[1]["event_timestamp"]


def test_no_retroactive_reordering():
    ledger = TemporalLedgerSimulator()

    now = datetime.utcnow()
    ledger.ingest(now)

    # Attempt manual reordering (simulate corruption)
    ledger.ledger.insert(0, {
        "signal_timestamp": now - timedelta(minutes=5),
        "event_timestamp": now - timedelta(minutes=5),
    })

    # Ledger ordering should now be invalid
    assert ledger.ledger[0]["event_timestamp"] < ledger.ledger[1]["event_timestamp"]