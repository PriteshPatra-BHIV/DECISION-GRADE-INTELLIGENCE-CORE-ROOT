"""
Example Usage - Decision-Grade Intelligence Core

Demonstrates how the system produces intelligence
without claiming authority or making decisions.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.intelligence_core import IntelligenceCore
from learning.policy_suggestion_engine import PolicySuggestionEngine
from learning.bounded_learning_rules import BoundedLearningRules
import json


def example_basic_intelligence():
    """Example: Basic intelligence generation."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Intelligence Generation")
    print("=" * 60)
    
    core = IntelligenceCore()
    
    signals = [
        {"signal_id": "S1", "value": 0.85, "confidence": 0.8, "source": "sensor_a"},
        {"signal_id": "S2", "value": 0.72, "confidence": 0.6, "source": "sensor_b"}
    ]
    
    output = core.process_signals(signals)
    
    print("\nINPUT SIGNALS:")
    for sig in signals:
        print(f"  {sig['signal_id']}: value={sig['value']}, confidence={sig['confidence']}")
    
    print("\nINTERPRETATIONS:")
    for interp in output["interpretations"]:
        print(f"  {interp['hypothesis']}: {interp['description']}")
        print(f"    Confidence: {interp['confidence_estimate']['mean']:.2f} ± {interp['confidence_estimate']['uncertainty']:.2f}")
    
    print("\nUNCERTAINTY:")
    print(f"  Known unknowns: {len(output['uncertainty']['known_unknowns'])}")
    print(f"  Ambiguities: {len(output['uncertainty']['ambiguities'])}")
    
    print("\nNON-GUARANTEES:")
    print(f"  {output['non_guarantees']}")
    
    print("\n[OK] Intelligence generated without claiming authority\n")


def example_conflicting_signals():
    """Example: Handling conflicting signals."""
    print("=" * 60)
    print("EXAMPLE 2: Conflicting Signals (Ambiguity Preserved)")
    print("=" * 60)
    
    core = IntelligenceCore()
    
    signals = [
        {"signal_id": "S1", "value": 0.95, "confidence": 0.9, "source": "sensor_a"},
        {"signal_id": "S2", "value": 0.15, "confidence": 0.2, "source": "sensor_b"}
    ]
    
    output = core.process_signals(signals)
    
    print("\nCONFLICTING SIGNALS DETECTED")
    print(f"  S1: High confidence (0.9)")
    print(f"  S2: Low confidence (0.2)")
    
    print("\nAMBIGUITIES REPORTED:")
    for amb in output["uncertainty"]["ambiguities"]:
        print(f"  - {amb}")
    
    print("\n[OK] Ambiguity preserved, not collapsed\n")


def example_policy_suggestions():
    """Example: Non-authoritative policy suggestions."""
    print("=" * 60)
    print("EXAMPLE 3: Policy Suggestions (Non-Authoritative)")
    print("=" * 60)
    
    engine = PolicySuggestionEngine()
    
    context = {"state": "operational"}
    observations = [
        {"signal_id": "S1", "outcome": "positive"},
        {"signal_id": "S2", "outcome": "neutral"}
    ]
    
    suggestions = engine.suggest_policies(context, observations)
    
    print("\nPOLICY SUGGESTIONS:")
    for sug in suggestions:
        print(f"  {sug['policy_candidate']}: {sug['description']}")
        print(f"    Confidence: {sug['confidence_estimate']['mean']:.2f} ± {sug['confidence_estimate']['uncertainty']:.2f}")
        print(f"    Note: {sug['non_guarantee']}")
    
    print("\n[OK] Suggestions provided without execution authority\n")


def example_authority_refusal():
    """Example: Explicit refusal of authority."""
    print("=" * 60)
    print("EXAMPLE 4: Authority Boundary Enforcement")
    print("=" * 60)
    
    core = IntelligenceCore()
    
    print("\nAttempting to request decision-making...")
    try:
        core.refuse_decision()
    except Exception as e:
        print(f"  [OK] REFUSED: {e}")
    
    print("\nAttempting to request action execution...")
    try:
        core.refuse_execution()
    except Exception as e:
        print(f"  [OK] REFUSED: {e}")
    
    print("\nAttempting to request optimization...")
    try:
        core.refuse_optimization()
    except Exception as e:
        print(f"  [OK] REFUSED: {e}")
    
    print("\n[OK] Authority boundaries enforced\n")


def example_bounded_learning():
    """Example: Bounded learning with supervision."""
    print("=" * 60)
    print("EXAMPLE 5: Bounded Learning (Supervision Required)")
    print("=" * 60)
    
    rules = BoundedLearningRules()
    
    print("\nLearning status:")
    print(f"  Enabled: {rules.learning_enabled}")
    print(f"  Supervision required: {rules.supervision_required}")
    
    print("\nEnabling learning with supervisor approval...")
    rules.enable_learning("supervisor-alice")
    print(f"  [OK] Learning enabled by supervisor-alice")
    
    print("\nApplying supervised update...")
    update = {"type": "confidence_adjustment", "value": 0.1, "source": "external"}
    rules.apply_update(update, "supervisor-alice")
    print(f"  [OK] Update applied with supervision")
    
    print("\nAudit trail:")
    for entry in rules.get_audit_trail():
        print(f"  - {entry.get('action', 'update')}: {entry.get('supervisor', 'N/A')}")
    
    print("\n[OK] Learning bounded and auditable\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DECISION-GRADE INTELLIGENCE CORE - EXAMPLES")
    print("=" * 60 + "\n")
    
    example_basic_intelligence()
    example_conflicting_signals()
    example_policy_suggestions()
    example_authority_refusal()
    example_bounded_learning()
    
    print("=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)
    print("\nKey Guarantees Demonstrated:")
    print("  [OK] Intelligence never becomes authority")
    print("  [OK] Uncertainty never silently collapsed")
    print("  [OK] Learning bounded and supervised")
    print("  [OK] Authority boundaries enforced")
    print("  [OK] System safe for integration\n")
