"""
Orchestrator → DGIC Integration Examples
Owner: Pritesh Patra
Consumer: Aakanksha Parab (AI Being Orchestrator)

This file demonstrates concrete examples of how to call DGIC from the Orchestrator.
"""

from orchestrator_dgic_integration import OrchestratorDGICClient, DGICIntegrationError
import json


def example_1_normal_safe_scenario():
    """
    Example 1: Normal scenario with safe signals
    Expected: PROCEED decision
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Normal Safe Scenario")
    print("="*80)
    
    client = OrchestratorDGICClient(dgic_url="http://localhost:8000")
    
    # Create signals indicating safe operation
    signals = [
        client.create_signal(
            signal_id="sig_001",
            signal_type="SAFE",
            priority=0.9,
            source="agent_alpha",
            metadata={"confidence": 0.95}
        ),
        client.create_signal(
            signal_id="sig_002",
            signal_type="SAFE",
            priority=0.85,
            source="agent_beta",
            metadata={"confidence": 0.88}
        )
    ]
    
    print("\nOrchestrator Input:")
    print(json.dumps({"signals": signals}, indent=2))
    
    try:
        response = client.evaluate_decision(signals=signals)
        print("\nDGIC Output:")
        print(json.dumps(response, indent=2))
        print(f"\n✓ Decision: {response['decision']}")
        print(f"✓ Epistemic State: {response['epistemic_state']}")
        print(f"✓ Confidence: {response['confidence']}")
        
    except DGICIntegrationError as e:
        print(f"\n✗ Error: {e}")


def example_2_threat_scenario():
    """
    Example 2: High-priority threat detected
    Expected: ESCALATE decision
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Threat Detection Scenario")
    print("="*80)
    
    client = OrchestratorDGICClient(dgic_url="http://localhost:8000")
    
    signals = [
        client.create_signal(
            signal_id="sig_threat_001",
            signal_type="THREAT",
            priority=0.95,
            source="security_agent",
            metadata={"threat_type": "intrusion_attempt"}
        ),
        client.create_signal(
            signal_id="sig_threat_002",
            signal_type="THREAT",
            priority=0.88,
            source="anomaly_detector",
            metadata={"anomaly_score": 0.92}
        )
    ]
    
    print("\nOrchestrator Input:")
    print(json.dumps({"signals": signals}, indent=2))
    
    try:
        response = client.evaluate_decision(signals=signals)
        print("\nDGIC Output:")
        print(json.dumps(response, indent=2))
        print(f"\n✓ Decision: {response['decision']}")
        print(f"✓ Epistemic State: {response['epistemic_state']}")
        print(f"✓ Confidence: {response['confidence']}")
        
    except DGICIntegrationError as e:
        print(f"\n✗ Error: {e}")


def example_3_contradictory_signals():
    """
    Example 3: Contradictory signals (threat vs safe)
    Expected: ESCALATE decision with CONTRADICTORY state
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Contradictory Signals Scenario")
    print("="*80)
    
    client = OrchestratorDGICClient(dgic_url="http://localhost:8000")
    
    signals = [
        client.create_signal(
            signal_id="sig_threat_001",
            signal_type="THREAT",
            priority=0.75,
            source="agent_alpha"
        ),
        client.create_signal(
            signal_id="sig_safe_001",
            signal_type="SAFE",
            priority=0.70,
            source="agent_beta"
        ),
        client.create_signal(
            signal_id="sig_threat_002",
            signal_type="THREAT",
            priority=0.65,
            source="agent_gamma"
        )
    ]
    
    print("\nOrchestrator Input:")
    print(json.dumps({"signals": signals}, indent=2))
    
    try:
        response = client.evaluate_decision(signals=signals)
        print("\nDGIC Output:")
        print(json.dumps(response, indent=2))
        print(f"\n✓ Decision: {response['decision']}")
        print(f"✓ Epistemic State: {response['epistemic_state']}")
        print(f"✓ Confidence: {response['confidence']}")
        
    except DGICIntegrationError as e:
        print(f"\n✗ Error: {e}")


def example_4_ambiguous_scenario():
    """
    Example 4: Ambiguous signals (moderate confidence)
    Expected: HOLD decision
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Ambiguous Scenario")
    print("="*80)
    
    client = OrchestratorDGICClient(dgic_url="http://localhost:8000")
    
    signals = [
        client.create_signal(
            signal_id="sig_001",
            signal_type="SAFE",
            priority=0.6,
            source="agent_alpha"
        ),
        client.create_signal(
            signal_id="sig_002",
            signal_type="UNKNOWN",
            priority=0.5,
            source="agent_beta"
        )
    ]
    
    print("\nOrchestrator Input:")
    print(json.dumps({"signals": signals}, indent=2))
    
    try:
        response = client.evaluate_decision(signals=signals)
        print("\nDGIC Output:")
        print(json.dumps(response, indent=2))
        print(f"\n✓ Decision: {response['decision']}")
        print(f"✓ Epistemic State: {response['epistemic_state']}")
        print(f"✓ Confidence: {response['confidence']}")
        
    except DGICIntegrationError as e:
        print(f"\n✗ Error: {e}")


def example_5_insufficient_data():
    """
    Example 5: Insufficient signals
    Expected: REQUEST_MORE_DATA decision
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Insufficient Data Scenario")
    print("="*80)
    
    client = OrchestratorDGICClient(dgic_url="http://localhost:8000")
    
    signals = [
        client.create_signal(
            signal_id="sig_001",
            signal_type="UNKNOWN",
            priority=0.3,
            source="agent_alpha"
        )
    ]
    
    print("\nOrchestrator Input:")
    print(json.dumps({"signals": signals}, indent=2))
    
    try:
        response = client.evaluate_decision(signals=signals)
        print("\nDGIC Output:")
        print(json.dumps(response, indent=2))
        print(f"\n✓ Decision: {response['decision']}")
        print(f"✓ Epistemic State: {response['epistemic_state']}")
        print(f"✓ Confidence: {response['confidence']}")
        
    except DGICIntegrationError as e:
        print(f"\n✗ Error: {e}")


def example_6_error_handling():
    """
    Example 6: Error handling - invalid signal type
    Expected: DGICIntegrationError
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: Error Handling - Invalid Signal")
    print("="*80)
    
    client = OrchestratorDGICClient(dgic_url="http://localhost:8000")
    
    try:
        # This should raise an error due to invalid signal type
        signal = client.create_signal(
            signal_id="sig_001",
            signal_type="INVALID_TYPE",  # Invalid
            priority=0.8,
            source="agent_alpha"
        )
        print(f"\n✗ Should have raised error but got: {signal}")
        
    except ValueError as e:
        print(f"\n✓ Correctly caught error: {e}")


def example_7_custom_execution_id():
    """
    Example 7: Using custom execution_id for tracking
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: Custom Execution ID")
    print("="*80)
    
    client = OrchestratorDGICClient(dgic_url="http://localhost:8000")
    
    custom_execution_id = "550e8400-e29b-41d4-a716-446655440000"
    
    signals = [
        client.create_signal(
            signal_id="sig_001",
            signal_type="SAFE",
            priority=0.9,
            source="agent_alpha"
        ),
        client.create_signal(
            signal_id="sig_002",
            signal_type="SAFE",
            priority=0.85,
            source="agent_beta"
        )
    ]
    
    print(f"\nUsing custom execution_id: {custom_execution_id}")
    print("\nOrchestrator Input:")
    print(json.dumps({"execution_id": custom_execution_id, "signals": signals}, indent=2))
    
    try:
        response = client.evaluate_decision(
            signals=signals,
            execution_id=custom_execution_id
        )
        print("\nDGIC Output:")
        print(json.dumps(response, indent=2))
        print(f"\n✓ Execution ID preserved: {response['execution_id'] == custom_execution_id}")
        
    except DGICIntegrationError as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("ORCHESTRATOR → DGIC INTEGRATION EXAMPLES")
    print("="*80)
    print("\nNOTE: Ensure DGIC service is running at http://localhost:8000")
    print("Start with: uvicorn dgic_api:app --reload")
    
    # Run all examples
    example_1_normal_safe_scenario()
    example_2_threat_scenario()
    example_3_contradictory_signals()
    example_4_ambiguous_scenario()
    example_5_insufficient_data()
    example_6_error_handling()
    example_7_custom_execution_id()
    
    print("\n" + "="*80)
    print("ALL EXAMPLES COMPLETED")
    print("="*80)
