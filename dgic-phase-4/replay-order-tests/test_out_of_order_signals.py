from datetime import datetime, timedelta


class TemporalLedgerSimulator:
    """
    Simplified ledger simulator to test out-of-order signal handling.
    """

    def __init__(self):
        self.ledger = []

    def ingest_signal(self, signal_timestamp):
        event_timestamp = datetime.utcnow()

        entry = {
            "signal_timestamp": signal_timestamp,
            "event_timestamp": event_timestamp,
        }

        # Enforce ledger append-only behavior
        if self.ledger:
            if event_timestamp <= self.ledger[-1]["event_timestamp"]:
                raise Exception("Ledger ordering violation.")

        self.ledger.append(entry)


def test_out_of_order_signal_arrival():
    ledger = TemporalLedgerSimulator()

    now = datetime.utcnow()

    # First signal (newer external event)
    ledger.ingest_signal(now)

    # Late-arriving signal (older external event)
    older_signal_time = now - timedelta(minutes=10)
    ledger.ingest_signal(older_signal_time)

    if len(ledger.ledger) == 2:
        print("PASS: Out-of-order signal accepted without rewriting history.")
    else:
        print("FAIL: Ledger corrupted.")


def test_no_retroactive_insertion():
    ledger = TemporalLedgerSimulator()

    now = datetime.utcnow()

    ledger.ingest_signal(now)

    # Attempt manual retroactive insertion
    try:
        ledger.ledger.insert(0, {
            "signal_timestamp": now - timedelta(minutes=5),
            "event_timestamp": now - timedelta(minutes=5),
        })
        print("FAIL: Retroactive insertion should not be allowed.")
    except Exception:
        print("PASS: Retroactive insertion blocked.")


if __name__ == "__main__":
    test_out_of_order_signal_arrival()
    test_no_retroactive_insertion()
