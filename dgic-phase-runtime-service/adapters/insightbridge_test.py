from insightbridge_adapter import InsightBridgeAdapter

adapter = InsightBridgeAdapter()

signals = [
    {
        "signal_id": "A1",
        "type": "ANOMALY",
        "value": 0.4
    },
    {
        "signal_id": "S1",
        "type": "THREAT",
        "value": 0.6
    }
]

result = adapter.send_signal(signals)

print(result)