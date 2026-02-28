"""
API Usage Example

Demonstrates public API for external system integration.
"""

from api import create_api

# Create API instance
api = create_api()

# Example 1: Process signals
print("=" * 60)
print("API EXAMPLE: Signal Processing")
print("=" * 60)

signals = [
    {"signal_id": "S1", "value": 0.85, "confidence": 0.8, "source": "sensor_a"},
    {"signal_id": "S2", "value": 0.72, "confidence": 0.6, "source": "sensor_b"}
]

output = api.process_signals(signals)

print(f"\nProcessed {len(signals)} signals")
print(f"Generated {len(output['interpretations'])} interpretations")
print(f"Uncertainty preserved: {len(output['uncertainty']['known_unknowns'])} unknowns")
print(f"Authority claimed: NO (guaranteed by contract)")

# Example 2: Get system status
print("\n" + "=" * 60)
print("API EXAMPLE: System Status")
print("=" * 60)

status = api.get_system_status()
print(f"\nLearning enabled: {status['learning_enabled']}")
print(f"Supervision required: {status['supervision_required']}")
print(f"Pending approvals: {status['pending_approvals']}")
print(f"Refusals issued: {status['refusal_count']}")

# Example 3: Policy suggestions
print("\n" + "=" * 60)
print("API EXAMPLE: Policy Suggestions")
print("=" * 60)

context = {"state": "operational"}
observations = [{"signal_id": "S1", "outcome": "positive"}]

suggestions = api.suggest_policies(context, observations)
print(f"\nGenerated {len(suggestions)} policy suggestions")
print(f"All suggestions are: HYPOTHETICAL (non-binding)")
print(f"Execution authority: NONE (structurally excluded)")

print("\n" + "=" * 60)
print("API ready for integration")
print("=" * 60)
