"""
DGIC → Enforcement Integration Examples
Owner: Pritesh Patra
Consumer: Rajaryan Verma (Enforcement Engine)

This file demonstrates concrete examples of how Enforcement consumes DGIC decisions.
"""

from enforcement_dgic_integration import EnforcementDGICClient, consume_dgic_decision
import json


def example_1_proceed_to_allow():
    """
    Example 1: PROCEED decision → allow() action
    Scenario: High confidence safe signals
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: PROCEED → allow()")
    print("="*80)
    
    # Simulated DGIC response
    dgic_response = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440001",
        "timestamp": 1704067200150,
        "decision": "PROCEED",
        "confidence": 0.92,
        "epistemic_state": "CERTAIN",
        "collapse_trigger": "dominance",
        "execution_hash": "a3f5b8c9d2e1f4a7b6c5d8e9f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0",
        "processing_time_ms": 45
    }
    
    print("\nDGIC Output:")
    print(json.dumps(dgic_response, indent=2))
    
    client = EnforcementDGICClient()
    
    # Map decision to action
    action = client.map_decision_to_action(dgic_response)
    print("\nEnforcement Action Mapping:")
    print(json.dumps(action, indent=2))
    
    # Execute action
    result = client.execute_action(action)
    print("\nEnforcement Execution Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Decision: {dgic_response['decision']}")
    print(f"✓ Action: {action['action']}")
    print(f"✓ Status: {result['status']}")


def example_2_escalate_threat():
    """
    Example 2: ESCALATE decision → escalate() action
    Scenario: High confidence threat detected
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: ESCALATE (Threat) → escalate()")
    print("="*80)
    
    dgic_response = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440002",
        "timestamp": 1704067200250,
        "decision": "ESCALATE",
        "confidence": 0.95,
        "epistemic_state": "CERTAIN",
        "collapse_trigger": "dominance",
        "execution_hash": "b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6",
        "processing_time_ms": 52
    }
    
    print("\nDGIC Output:")
    print(json.dumps(dgic_response, indent=2))
    
    client = EnforcementDGICClient()
    action = client.map_decision_to_action(dgic_response)
    print("\nEnforcement Action Mapping:")
    print(json.dumps(action, indent=2))
    
    result = client.execute_action(action)
    print("\nEnforcement Execution Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Decision: {dgic_response['decision']}")
    print(f"✓ Action: {action['action']}")
    print(f"✓ Status: {result['status']}")


def example_3_escalate_contradiction():
    """
    Example 3: ESCALATE decision → escalate() action
    Scenario: Contradictory signals detected
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: ESCALATE (Contradiction) → escalate()")
    print("="*80)
    
    dgic_response = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440003",
        "timestamp": 1704067200350,
        "decision": "ESCALATE",
        "confidence": 0.5,
        "epistemic_state": "CONTRADICTORY",
        "collapse_trigger": "none",
        "execution_hash": "c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7",
        "processing_time_ms": 48
    }
    
    print("\nDGIC Output:")
    print(json.dumps(dgic_response, indent=2))
    
    client = EnforcementDGICClient()
    action = client.map_decision_to_action(dgic_response)
    print("\nEnforcement Action Mapping:")
    print(json.dumps(action, indent=2))
    
    result = client.execute_action(action)
    print("\nEnforcement Execution Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Decision: {dgic_response['decision']}")
    print(f"✓ Action: {action['action']}")
    print(f"✓ Status: {result['status']}")
    print(f"✓ Reason: Contradictory signals require human review")


def example_4_hold_to_delay():
    """
    Example 4: HOLD decision → delay() action
    Scenario: Ambiguous signals
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: HOLD → delay()")
    print("="*80)
    
    dgic_response = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440004",
        "timestamp": 1704067200450,
        "decision": "HOLD",
        "confidence": 0.65,
        "epistemic_state": "AMBIGUOUS",
        "collapse_trigger": "none",
        "execution_hash": "d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8",
        "processing_time_ms": 43
    }
    
    print("\nDGIC Output:")
    print(json.dumps(dgic_response, indent=2))
    
    client = EnforcementDGICClient()
    action = client.map_decision_to_action(dgic_response)
    print("\nEnforcement Action Mapping:")
    print(json.dumps(action, indent=2))
    
    result = client.execute_action(action)
    print("\nEnforcement Execution Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Decision: {dgic_response['decision']}")
    print(f"✓ Action: {action['action']}")
    print(f"✓ Status: {result['status']}")


def example_5_request_more_data():
    """
    Example 5: REQUEST_MORE_DATA decision → request_input() action
    Scenario: Insufficient signals
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: REQUEST_MORE_DATA → request_input()")
    print("="*80)
    
    dgic_response = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440005",
        "timestamp": 1704067200550,
        "decision": "REQUEST_MORE_DATA",
        "confidence": 0.3,
        "epistemic_state": "INSUFFICIENT",
        "collapse_trigger": "none",
        "execution_hash": "e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9",
        "processing_time_ms": 38
    }
    
    print("\nDGIC Output:")
    print(json.dumps(dgic_response, indent=2))
    
    client = EnforcementDGICClient()
    action = client.map_decision_to_action(dgic_response)
    print("\nEnforcement Action Mapping:")
    print(json.dumps(action, indent=2))
    
    result = client.execute_action(action)
    print("\nEnforcement Execution Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Decision: {dgic_response['decision']}")
    print(f"✓ Action: {action['action']}")
    print(f"✓ Status: {result['status']}")


def example_6_error_to_fail_safe():
    """
    Example 6: ERROR decision → fail_safe() action
    Scenario: DGIC processing failure
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: ERROR → fail_safe()")
    print("="*80)
    
    dgic_response = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440006",
        "timestamp": 1704067200650,
        "decision": "ERROR",
        "confidence": 0.0,
        "epistemic_state": "INSUFFICIENT",
        "collapse_trigger": "none",
        "execution_hash": "f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0",
        "processing_time_ms": 0
    }
    
    print("\nDGIC Output:")
    print(json.dumps(dgic_response, indent=2))
    
    client = EnforcementDGICClient()
    action = client.map_decision_to_action(dgic_response)
    print("\nEnforcement Action Mapping:")
    print(json.dumps(action, indent=2))
    
    result = client.execute_action(action)
    print("\nEnforcement Execution Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Decision: {dgic_response['decision']}")
    print(f"✓ Action: {action['action']}")
    print(f"✓ Status: {result['status']}")
    print(f"✓ Safety: Operation blocked due to error")


def example_7_override_mechanism():
    """
    Example 7: Override mechanism
    Scenario: Human operator overrides DGIC decision
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: Override Mechanism")
    print("="*80)
    
    dgic_response = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440007",
        "timestamp": 1704067200750,
        "decision": "HOLD",
        "confidence": 0.65,
        "epistemic_state": "AMBIGUOUS",
        "collapse_trigger": "none",
        "execution_hash": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
        "processing_time_ms": 44
    }
    
    print("\nDGIC Output:")
    print(json.dumps(dgic_response, indent=2))
    
    client = EnforcementDGICClient(enable_override=True)
    action = client.map_decision_to_action(dgic_response)
    print("\nEnforcement Action Mapping (Original):")
    print(json.dumps(action, indent=2))
    
    # Human operator decides to allow despite HOLD recommendation
    print("\n⚠️  Human operator applies override: HOLD → allow")
    result = client.execute_action(action, override="allow")
    print("\nEnforcement Execution Result (With Override):")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Original Decision: {dgic_response['decision']}")
    print(f"✓ Original Action: delay")
    print(f"✓ Override Action: {result['action']}")
    print(f"✓ Status: {result['status']}")
    print(f"✓ Override Logged: {result['override_applied']}")


def example_8_execution_tracking():
    """
    Example 8: Execution tracking with execution_id
    Scenario: Track actions across multiple decisions
    """
    print("\n" + "="*80)
    print("EXAMPLE 8: Execution Tracking")
    print("="*80)
    
    client = EnforcementDGICClient()
    
    # Process multiple decisions
    decisions = [
        {
            "execution_id": "550e8400-e29b-41d4-a716-446655440008",
            "decision": "PROCEED",
            "confidence": 0.9,
            "epistemic_state": "CERTAIN",
            "collapse_trigger": "dominance",
            "execution_hash": "hash1",
            "processing_time_ms": 40,
            "timestamp": 1704067200800
        },
        {
            "execution_id": "550e8400-e29b-41d4-a716-446655440009",
            "decision": "ESCALATE",
            "confidence": 0.95,
            "epistemic_state": "CERTAIN",
            "collapse_trigger": "dominance",
            "execution_hash": "hash2",
            "processing_time_ms": 45,
            "timestamp": 1704067200900
        }
    ]
    
    for dgic_response in decisions:
        action = client.map_decision_to_action(dgic_response)
        client.execute_action(action)
    
    # Retrieve logs
    print("\nAction Log:")
    for log_entry in client.get_action_log():
        print(json.dumps(log_entry, indent=2))
    
    print(f"\n✓ Total actions logged: {len(client.get_action_log())}")
    print(f"✓ Execution IDs tracked: {len(set(log['execution_id'] for log in client.get_action_log() if 'execution_id' in log))}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("DGIC → ENFORCEMENT INTEGRATION EXAMPLES")
    print("="*80)
    print("\nDemonstrating decision-to-action mapping and execution flow")
    
    # Run all examples
    example_1_proceed_to_allow()
    example_2_escalate_threat()
    example_3_escalate_contradiction()
    example_4_hold_to_delay()
    example_5_request_more_data()
    example_6_error_to_fail_safe()
    example_7_override_mechanism()
    example_8_execution_tracking()
    
    print("\n" + "="*80)
    print("ALL EXAMPLES COMPLETED")
    print("="*80)
