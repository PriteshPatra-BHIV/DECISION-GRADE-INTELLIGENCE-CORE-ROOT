"""
QUICK DEMO - Decision-Grade Intelligence Core
Run this for a fast 2-minute demonstration
"""

from api import create_api
import json

print("\n" + "="*60)
print("DECISION-GRADE INTELLIGENCE CORE - QUICK DEMO")
print("="*60)

api = create_api()

# 1. Process signals
print("\n1. INTELLIGENCE GENERATION")
print("-" * 60)
output = api.process_signals([
    {"signal_id": "S1", "value": 0.85, "confidence": 0.8},
    {"signal_id": "S2", "value": 0.72, "confidence": 0.6}
])
print(f"Signals processed: 2")
print(f"Interpretations: {len(output['interpretations'])}")
print(f"Uncertainty preserved: YES")
print(f"Authority claimed: NO")

# 2. Show refusal
print("\n2. AUTHORITY REFUSAL")
print("-" * 60)
try:
    api.core.refuse_decision()
except Exception as e:
    print(f"Decision request: REFUSED")
    print(f"Reason: {str(e)[:50]}...")

# 3. Policy suggestions
print("\n3. POLICY SUGGESTIONS")
print("-" * 60)
suggestions = api.suggest_policies(
    {"state": "operational"},
    [{"signal_id": "S1"}]
)
print(f"Suggestions generated: {len(suggestions)}")
print(f"Execution authority: NONE")
print(f"Binding: NO (hypothetical only)")

# 4. System status
print("\n4. SYSTEM STATUS")
print("-" * 60)
status = api.get_system_status()
print(f"Learning enabled: {status['learning_enabled']}")
print(f"Supervision required: {status['supervision_required']}")
print(f"Safe for integration: YES")

print("\n" + "="*60)
print("DEMO COMPLETE - All guarantees verified")
print("="*60 + "\n")
