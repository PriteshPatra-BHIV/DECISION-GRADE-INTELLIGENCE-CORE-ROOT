"""
DGIC → InsightBridge Integration Examples
Owner: Pritesh Patra
Consumer: Vijay Dhawan (InsightBridge)

This file demonstrates concrete examples of how InsightBridge consumes DGIC trace data.
"""

from insightbridge_dgic_integration import InsightBridgeDGICClient, consume_dgic_trace
import json


def example_1_trace_verification():
    """
    Example 1: Verify trace data integrity using trace_hash
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Trace Verification")
    print("="*80)
    
    # Simulated DGIC trace
    trace_data = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440001",
        "timestamp": 1704067200150,
        "input_signals": [
            {"id": "sig_001", "type": "SAFE", "priority": 0.9, "timestamp": 1704067199000},
            {"id": "sig_002", "type": "SAFE", "priority": 0.85, "timestamp": 1704067199500}
        ],
        "reasoning_trace": [
            {"step": 1, "operation": "signal_aggregation", "result": {"threat_weight": 0.0, "safe_weight": 1.75}, "timestamp": 1704067200010},
            {"step": 2, "operation": "state_computation", "result": {"state": "CERTAIN", "confidence": 0.92}, "timestamp": 1704067200025}
        ],
        "collapse_event": {
            "occurred": True,
            "trigger": "dominance",
            "timestamp": 1704067200030,
            "selected_state": "PROCEED",
            "eliminated_states": [],
            "reason": "Collapse triggered by dominance"
        },
        "final_state": {
            "decision": "PROCEED",
            "confidence": 0.92,
            "epistemic_state": "CERTAIN"
        },
        "execution_hash": "a3f5b8c9d2e1f4a7b6c5d8e9f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0",
        "trace_hash": "b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6"
    }
    
    print("\nDGIC Trace Data:")
    print(json.dumps(trace_data, indent=2))
    
    client = InsightBridgeDGICClient()
    verification = client.verify_trace(trace_data)
    
    print("\nTrace Verification Result:")
    print(json.dumps(verification, indent=2))
    
    print(f"\n✓ Trace Valid: {verification['valid']}")
    print(f"✓ Execution ID: {verification['execution_id']}")


def example_2_store_trace():
    """
    Example 2: Store trace data immutably
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Store Trace Data")
    print("="*80)
    
    trace_data = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440002",
        "timestamp": 1704067200250,
        "input_signals": [
            {"id": "sig_003", "type": "THREAT", "priority": 0.95, "timestamp": 1704067199000}
        ],
        "reasoning_trace": [
            {"step": 1, "operation": "signal_aggregation", "result": {"threat_weight": 0.95, "safe_weight": 0.0}, "timestamp": 1704067200010}
        ],
        "collapse_event": {
            "occurred": True,
            "trigger": "dominance",
            "timestamp": 1704067200030,
            "selected_state": "ESCALATE",
            "eliminated_states": [],
            "reason": "Collapse triggered by dominance"
        },
        "final_state": {
            "decision": "ESCALATE",
            "confidence": 0.95,
            "epistemic_state": "CERTAIN"
        },
        "execution_hash": "c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7",
        "trace_hash": "d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8"
    }
    
    print("\nStoring Trace:")
    print(json.dumps({"execution_id": trace_data["execution_id"], "decision": trace_data["final_state"]["decision"]}, indent=2))
    
    client = InsightBridgeDGICClient()
    result = client.store_trace(trace_data, verify_first=True)
    
    print("\nStorage Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Stored: {result['stored']}")
    print(f"✓ Execution ID: {result['execution_id']}")


def example_3_retrieve_trace():
    """
    Example 3: Retrieve trace by execution_id
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Retrieve Trace by Execution ID")
    print("="*80)
    
    client = InsightBridgeDGICClient()
    
    # Store multiple traces
    traces = [
        {
            "execution_id": "550e8400-e29b-41d4-a716-446655440003",
            "timestamp": 1704067200350,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {"occurred": False, "trigger": "none", "timestamp": 0, "selected_state": None, "eliminated_states": [], "reason": ""},
            "final_state": {"decision": "PROCEED", "confidence": 0.9, "epistemic_state": "CERTAIN"},
            "execution_hash": "hash1",
            "trace_hash": "trace_hash1"
        },
        {
            "execution_id": "550e8400-e29b-41d4-a716-446655440004",
            "timestamp": 1704067200450,
            "input_signals": [],
            "reasoning_trace": [],
            "collapse_event": {"occurred": False, "trigger": "none", "timestamp": 0, "selected_state": None, "eliminated_states": [], "reason": ""},
            "final_state": {"decision": "ESCALATE", "confidence": 0.95, "epistemic_state": "CERTAIN"},
            "execution_hash": "hash2",
            "trace_hash": "trace_hash2"
        }
    ]
    
    for trace in traces:
        client.store_trace(trace, verify_first=False)
    
    # Retrieve specific trace
    execution_id = "550e8400-e29b-41d4-a716-446655440003"
    retrieved = client.retrieve_trace(execution_id)
    
    print(f"\nRetrieving trace for: {execution_id}")
    print("\nRetrieved Trace:")
    print(json.dumps(retrieved, indent=2))
    
    print(f"\n✓ Found: {retrieved is not None}")
    print(f"✓ Decision: {retrieved['final_state']['decision']}")


def example_4_execution_hash_verification():
    """
    Example 4: Verify execution_hash matches between trace and DGIC response
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Execution Hash Verification")
    print("="*80)
    
    dgic_response = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440005",
        "timestamp": 1704067200550,
        "decision": "HOLD",
        "confidence": 0.65,
        "epistemic_state": "AMBIGUOUS",
        "collapse_trigger": "none",
        "execution_hash": "e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9",
        "processing_time_ms": 43
    }
    
    trace_data = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440005",
        "timestamp": 1704067200550,
        "input_signals": [],
        "reasoning_trace": [],
        "collapse_event": {"occurred": False, "trigger": "none", "timestamp": 0, "selected_state": None, "eliminated_states": [], "reason": ""},
        "final_state": {"decision": "HOLD", "confidence": 0.65, "epistemic_state": "AMBIGUOUS"},
        "execution_hash": "e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9",
        "trace_hash": "f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0"
    }
    
    print("\nDGIC Response execution_hash:", dgic_response["execution_hash"])
    print("Trace execution_hash:", trace_data["execution_hash"])
    
    client = InsightBridgeDGICClient()
    verification = client.verify_execution_hash(trace_data, dgic_response)
    
    print("\nExecution Hash Verification:")
    print(json.dumps(verification, indent=2))
    
    print(f"\n✓ Hashes Match: {verification['match']}")


def example_5_cross_system_correlation():
    """
    Example 5: Correlate data across systems using execution_id
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Cross-System Correlation")
    print("="*80)
    
    client = InsightBridgeDGICClient()
    
    # Store trace
    trace_data = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440006",
        "timestamp": 1704067200650,
        "input_signals": [
            {"id": "sig_005", "type": "SAFE", "priority": 0.9, "timestamp": 1704067199000},
            {"id": "sig_006", "type": "SAFE", "priority": 0.85, "timestamp": 1704067199500}
        ],
        "reasoning_trace": [
            {"step": 1, "operation": "signal_aggregation", "result": {}, "timestamp": 1704067200010},
            {"step": 2, "operation": "state_computation", "result": {}, "timestamp": 1704067200025}
        ],
        "collapse_event": {"occurred": True, "trigger": "dominance", "timestamp": 1704067200030, "selected_state": "PROCEED", "eliminated_states": [], "reason": "Collapse triggered by dominance"},
        "final_state": {"decision": "PROCEED", "confidence": 0.92, "epistemic_state": "CERTAIN"},
        "execution_hash": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
        "trace_hash": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3"
    }
    
    client.store_trace(trace_data, verify_first=False)
    
    # Correlate by execution_id
    execution_id = "550e8400-e29b-41d4-a716-446655440006"
    correlation = client.correlate_by_execution_id(execution_id)
    
    print(f"\nCorrelating data for execution_id: {execution_id}")
    print("\nCorrelation Result:")
    print(json.dumps(correlation, indent=2))
    
    print(f"\n✓ Found: {correlation['found']}")
    print(f"✓ Decision: {correlation['final_decision']}")
    print(f"✓ Input Signals: {len(correlation['input_signals'])}")
    print(f"✓ Reasoning Steps: {correlation['reasoning_steps']}")


def example_6_replay_verification():
    """
    Example 6: Verify replay consistency
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: Replay Verification")
    print("="*80)
    
    original_trace = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440007",
        "timestamp": 1704067200750,
        "input_signals": [],
        "reasoning_trace": [],
        "collapse_event": {"occurred": False, "trigger": "none", "timestamp": 0, "selected_state": None, "eliminated_states": [], "reason": ""},
        "final_state": {"decision": "PROCEED", "confidence": 0.9, "epistemic_state": "CERTAIN"},
        "execution_hash": "original_exec_hash_123",
        "trace_hash": "original_trace_hash_456"
    }
    
    replay_trace = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440007",
        "timestamp": 1704067200750,
        "input_signals": [],
        "reasoning_trace": [],
        "collapse_event": {"occurred": False, "trigger": "none", "timestamp": 0, "selected_state": None, "eliminated_states": [], "reason": ""},
        "final_state": {"decision": "PROCEED", "confidence": 0.9, "epistemic_state": "CERTAIN"},
        "execution_hash": "original_exec_hash_123",
        "trace_hash": "original_trace_hash_456"
    }
    
    print("\nOriginal Trace Hash:", original_trace["trace_hash"])
    print("Replay Trace Hash:", replay_trace["trace_hash"])
    
    client = InsightBridgeDGICClient()
    verification = client.replay_verification(original_trace, replay_trace)
    
    print("\nReplay Verification Result:")
    print(json.dumps(verification, indent=2))
    
    print(f"\n✓ Replay Valid: {verification['replay_valid']}")
    print(f"✓ Trace Hash Match: {verification['trace_hash_match']}")
    print(f"✓ Execution Hash Match: {verification['execution_hash_match']}")


def example_7_filter_traces():
    """
    Example 7: Filter traces by decision type
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: Filter Traces")
    print("="*80)
    
    client = InsightBridgeDGICClient()
    
    # Store multiple traces with different decisions
    traces = [
        {"execution_id": "exec_001", "timestamp": 0, "input_signals": [], "reasoning_trace": [], "collapse_event": {}, "final_state": {"decision": "PROCEED", "confidence": 0.9, "epistemic_state": "CERTAIN"}, "execution_hash": "h1", "trace_hash": "t1"},
        {"execution_id": "exec_002", "timestamp": 0, "input_signals": [], "reasoning_trace": [], "collapse_event": {}, "final_state": {"decision": "ESCALATE", "confidence": 0.95, "epistemic_state": "CERTAIN"}, "execution_hash": "h2", "trace_hash": "t2"},
        {"execution_id": "exec_003", "timestamp": 0, "input_signals": [], "reasoning_trace": [], "collapse_event": {}, "final_state": {"decision": "PROCEED", "confidence": 0.88, "epistemic_state": "CERTAIN"}, "execution_hash": "h3", "trace_hash": "t3"},
        {"execution_id": "exec_004", "timestamp": 0, "input_signals": [], "reasoning_trace": [], "collapse_event": {}, "final_state": {"decision": "HOLD", "confidence": 0.65, "epistemic_state": "AMBIGUOUS"}, "execution_hash": "h4", "trace_hash": "t4"}
    ]
    
    for trace in traces:
        client.store_trace(trace, verify_first=False)
    
    # Filter by decision
    escalate_traces = client.get_all_traces(filter_by={"decision": "ESCALATE"})
    proceed_traces = client.get_all_traces(filter_by={"decision": "PROCEED"})
    
    print(f"\nTotal traces stored: {len(client.get_all_traces())}")
    print(f"ESCALATE traces: {len(escalate_traces)}")
    print(f"PROCEED traces: {len(proceed_traces)}")
    
    print("\nESCALATE Traces:")
    for trace in escalate_traces:
        print(f"  - {trace['execution_id']}: {trace['final_state']['decision']}")


def example_8_convenience_function():
    """
    Example 8: Use convenience function for quick integration
    """
    print("\n" + "="*80)
    print("EXAMPLE 8: Convenience Function")
    print("="*80)
    
    trace_data = {
        "execution_id": "550e8400-e29b-41d4-a716-446655440008",
        "timestamp": 1704067200850,
        "input_signals": [],
        "reasoning_trace": [],
        "collapse_event": {"occurred": False, "trigger": "none", "timestamp": 0, "selected_state": None, "eliminated_states": [], "reason": ""},
        "final_state": {"decision": "PROCEED", "confidence": 0.9, "epistemic_state": "CERTAIN"},
        "execution_hash": "quick_hash",
        "trace_hash": "quick_trace_hash"
    }
    
    print("\nUsing convenience function to store trace:")
    result = consume_dgic_trace(trace_data, verify=False)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Stored: {result['stored']}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("DGIC → INSIGHTBRIDGE INTEGRATION EXAMPLES")
    print("="*80)
    print("\nDemonstrating trace consumption, verification, and correlation")
    
    # Run all examples
    example_1_trace_verification()
    example_2_store_trace()
    example_3_retrieve_trace()
    example_4_execution_hash_verification()
    example_5_cross_system_correlation()
    example_6_replay_verification()
    example_7_filter_traces()
    example_8_convenience_function()
    
    print("\n" + "="*80)
    print("ALL EXAMPLES COMPLETED")
    print("="*80)
