from orchestrator_adapter import OrchestratorAdapter

adapter = OrchestratorAdapter()

signals = [
    {
        "signal_id": "S1",
        "type": "THREAT",
        "value": 0.7
    }
]

result = adapter.evaluate_action(
    action_proposal="BLOCK_USER_ACCOUNT",
    signals=signals
)

print(result)