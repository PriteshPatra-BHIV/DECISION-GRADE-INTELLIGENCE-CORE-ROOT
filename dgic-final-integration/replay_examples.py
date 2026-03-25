"""
Phase 7: Replay System Examples
Demonstrates replay capabilities across all BHIV systems
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from replay_system import ReplaySystem, ReplayStatus
from insightbridge_dgic_integration import InsightBridgeDGICClient


def example_1_single_execution_replay():
    """Example 1: Replay single execution"""
    print("\n=== Example 1: Single Execution Replay ===")
    
    insightbridge = InsightBridgeDGICClient("http://localhost:8003")
    replay_system = ReplaySystem(insightbridge)
    
    execution_id = "550e8400-e29b-41d4-a716-446655440001"
    result = replay_system.replay_execution(execution_id)
    
    print(f"Execution ID: {result['execution_id']}")
    print(f"Replay Status: {result['replay_status']}")
    print(f"Timeline Events: {len(result['timeline'])}")
    print(f"Systems Involved: {list(result['system_states'].keys())}")
    print(f"Verification: {result['verification']}")


def example_2_batch_replay():
    """Example 2: Batch replay multiple executions"""
    print("\n=== Example 2: Batch Replay ===")
    
    insightbridge = InsightBridgeDGICClient("http://localhost:8003")
    replay_system = ReplaySystem(insightbridge)
    
    execution_ids = [
        "550e8400-e29b-41d4-a716-446655440001",
        "550e8400-e29b-41d4-a716-446655440002",
        "550e8400-e29b-41d4-a716-446655440003"
    ]
    
    result = replay_system.replay_batch(execution_ids)
    
    print(f"Total Executions: {result['total']}")
    print(f"Verified: {result['verified']}")
    print(f"Failed: {result['failed']}")
    
    for replay in result['results']:
        print(f"  - {replay['execution_id']}: {replay['replay_status']}")


def example_3_decision_chain_verification():
    """Example 3: Verify decision chain integrity"""
    print("\n=== Example 3: Decision Chain Verification ===")
    
    insightbridge = InsightBridgeDGICClient("http://localhost:8003")
    replay_system = ReplaySystem(insightbridge)
    
    execution_id = "550e8400-e29b-41d4-a716-446655440001"
    result = replay_system.verify_decision_chain(execution_id)
    
    print(f"Execution ID: {result['execution_id']}")
    print(f"Chain Valid: {result['chain_valid']}")
    print(f"Signal → Decision: {result['signal_to_decision']}")
    print(f"Decision → Action: {result['decision_to_action']}")
    print(f"Action → Trace: {result['action_to_trace']}")
    
    if result['errors']:
        print(f"Errors: {result['errors']}")


def example_4_timeline_reconstruction():
    """Example 4: Reconstruct execution timeline"""
    print("\n=== Example 4: Timeline Reconstruction ===")
    
    insightbridge = InsightBridgeDGICClient("http://localhost:8003")
    replay_system = ReplaySystem(insightbridge)
    
    execution_id = "550e8400-e29b-41d4-a716-446655440001"
    result = replay_system.replay_execution(execution_id)
    
    print(f"Execution ID: {execution_id}")
    print("Timeline:")
    
    for i, event in enumerate(result['timeline'], 1):
        print(f"  {i}. [{event['system']}] {event['action']}")
        print(f"     Timestamp: {event['timestamp']}")


def example_5_system_state_extraction():
    """Example 5: Extract system states"""
    print("\n=== Example 5: System State Extraction ===")
    
    insightbridge = InsightBridgeDGICClient("http://localhost:8003")
    replay_system = ReplaySystem(insightbridge)
    
    execution_id = "550e8400-e29b-41d4-a716-446655440001"
    result = replay_system.replay_execution(execution_id)
    
    print(f"Execution ID: {execution_id}")
    print("\nSystem States:")
    
    for system, state in result['system_states'].items():
        print(f"\n{system.upper()}:")
        for key, value in state.items():
            print(f"  {key}: {value}")


def example_6_execution_comparison():
    """Example 6: Compare two executions"""
    print("\n=== Example 6: Execution Comparison ===")
    
    insightbridge = InsightBridgeDGICClient("http://localhost:8003")
    replay_system = ReplaySystem(insightbridge)
    
    exec_id_1 = "550e8400-e29b-41d4-a716-446655440001"
    exec_id_2 = "550e8400-e29b-41d4-a716-446655440002"
    
    result = replay_system.compare_executions(exec_id_1, exec_id_2)
    
    print(f"Comparing: {result['execution_1']} vs {result['execution_2']}")
    print(f"Status Match: {result['status_match']}")
    print(f"Decision Match: {result['decision_match']}")
    print(f"Action Match: {result['action_match']}")
    
    if result['differences']:
        print(f"Differences: {result['differences']}")


def example_7_audit_trail_generation():
    """Example 7: Generate audit trail"""
    print("\n=== Example 7: Audit Trail Generation ===")
    
    insightbridge = InsightBridgeDGICClient("http://localhost:8003")
    replay_system = ReplaySystem(insightbridge)
    
    execution_id = "550e8400-e29b-41d4-a716-446655440001"
    audit = replay_system.audit_trail(execution_id)
    
    print(f"Audit Trail for: {audit['execution_id']}")
    print(f"Audit Timestamp: {audit['audit_timestamp']}")
    print(f"Replay Status: {audit['replay_status']}")
    print(f"\nTotal Events: {audit['summary']['total_events']}")
    print(f"Systems Involved: {audit['summary']['systems_involved']}")


def example_8_hash_verification():
    """Example 8: Verify trace hash integrity"""
    print("\n=== Example 8: Hash Verification ===")
    
    insightbridge = InsightBridgeDGICClient("http://localhost:8003")
    replay_system = ReplaySystem(insightbridge)
    
    execution_id = "550e8400-e29b-41d4-a716-446655440001"
    result = replay_system.replay_execution(execution_id)
    
    print(f"Execution ID: {execution_id}")
    print(f"Replay Status: {result['replay_status']}")
    
    if result['replay_status'] == ReplayStatus.HASH_MISMATCH.value:
        print("⚠️  Hash verification failed")
    elif result['replay_status'] == ReplayStatus.VERIFIED.value:
        print("✓ Hash verification passed")


if __name__ == "__main__":
    print("=" * 60)
    print("PHASE 7: REPLAY SYSTEM EXAMPLES")
    print("=" * 60)
    
    example_1_single_execution_replay()
    example_2_batch_replay()
    example_3_decision_chain_verification()
    example_4_timeline_reconstruction()
    example_5_system_state_extraction()
    example_6_execution_comparison()
    example_7_audit_trail_generation()
    example_8_hash_verification()
    
    print("\n" + "=" * 60)
    print("All replay examples completed!")
    print("=" * 60)
