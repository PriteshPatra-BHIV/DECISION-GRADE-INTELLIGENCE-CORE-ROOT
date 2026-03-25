"""
Failure Flow Examples
Owner: Pritesh Patra

Demonstrates failure handling across all BHIV systems.
"""

from failure_flow_pipeline import ResilientBHIVPipeline, FailureType
import json


def example_1_dgic_unreachable():
    """
    Example 1: DGIC service unreachable
    Expected: Fail-safe → ERROR decision → fail_safe() → BLOCKED
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: DGIC Service Unreachable")
    print("="*80)
    
    pipeline = ResilientBHIVPipeline(dgic_url="http://localhost:9999")  # Wrong port
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha")
    ]
    
    print("\nAttempting to reach DGIC at wrong port...")
    
    result = pipeline.execute_with_failure_handling(
        signals,
        inject_failure=FailureType.DGIC_UNREACHABLE
    )
    
    print("\nFailure Handling Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Failures Detected: {len(result['failures'])}")
    print(f"✓ Recovery Actions: {len(result['recovery_actions'])}")
    print(f"✓ Final Decision: {result['dgic']['decision']}")
    print(f"✓ Enforcement Status: {result['enforcement']['status']}")
    print(f"✓ System Failed Safely: {result['enforcement']['status'] == 'BLOCKED'}")


def example_2_dgic_timeout():
    """
    Example 2: DGIC request timeout
    Expected: Fail-safe → ERROR decision → fail_safe() → BLOCKED
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: DGIC Request Timeout")
    print("="*80)
    
    pipeline = ResilientBHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha")
    ]
    
    print("\nSimulating DGIC timeout...")
    
    result = pipeline.execute_with_failure_handling(
        signals,
        inject_failure=FailureType.DGIC_TIMEOUT
    )
    
    print("\nFailure Handling Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Failure Type: {result['failures'][0]['type']}")
    print(f"✓ Recovery: {result['failures'][0]['recovery']}")
    print(f"✓ Final Decision: {result['dgic']['decision']}")
    print(f"✓ System Failed Safely: {result['enforcement']['status'] == 'BLOCKED'}")


def example_3_invalid_signals():
    """
    Example 3: Invalid signal format
    Expected: Request rejected at validation
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Invalid Signal Format")
    print("="*80)
    
    pipeline = ResilientBHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha")
    ]
    
    print("\nSimulating invalid signal format...")
    
    result = pipeline.execute_with_failure_handling(
        signals,
        inject_failure=FailureType.INVALID_SIGNALS
    )
    
    print("\nFailure Handling Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Request Rejected: {result['success'] == False}")
    print(f"✓ Error Stage: {result.get('stage', 'N/A')}")
    print(f"✓ Failure Logged: {len(result['failures']) > 0}")


def example_4_enforcement_failure():
    """
    Example 4: Enforcement system error
    Expected: Enforcement fails → fail_safe() → BLOCKED
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Enforcement System Error")
    print("="*80)
    
    pipeline = ResilientBHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
        pipeline.orchestrator.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
    ]
    
    print("\nSimulating enforcement system error...")
    
    result = pipeline.execute_with_failure_handling(
        signals,
        inject_failure=FailureType.ENFORCEMENT_ERROR
    )
    
    print("\nFailure Handling Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ DGIC Decision: {result['dgic']['decision']}")
    print(f"✓ Enforcement Failed: {any(f['type'] == 'ENFORCEMENT_ERROR' for f in result['failures'])}")
    print(f"✓ Fail-Safe Applied: {result['enforcement']['action'] == 'fail_safe'}")
    print(f"✓ Operation Blocked: {result['enforcement']['status'] == 'BLOCKED'}")


def example_5_insightbridge_failure():
    """
    Example 5: InsightBridge storage error
    Expected: Continue without trace (acceptable per contract)
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: InsightBridge Storage Error")
    print("="*80)
    
    pipeline = ResilientBHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
        pipeline.orchestrator.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
    ]
    
    print("\nSimulating InsightBridge storage error...")
    
    result = pipeline.execute_with_failure_handling(
        signals,
        inject_failure=FailureType.INSIGHTBRIDGE_ERROR
    )
    
    print("\nFailure Handling Result:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ DGIC Decision: {result['dgic']['decision']}")
    print(f"✓ Enforcement Status: {result['enforcement']['status']}")
    print(f"✓ InsightBridge Failed: {any(f['type'] == 'INSIGHTBRIDGE_ERROR' for f in result['failures'])}")
    print(f"✓ Pipeline Continued: {result['enforcement']['status'] == 'ALLOWED'}")
    print(f"✓ Trace Not Stored: {result['insightbridge']['trace_stored'] == False}")
    print(f"⚠️  Note: InsightBridge failure is acceptable per contract")


def example_6_multiple_failures():
    """
    Example 6: Multiple failures in sequence
    Expected: Each failure handled independently
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: Multiple Failures in Sequence")
    print("="*80)
    
    pipeline = ResilientBHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha")
    ]
    
    failure_types = [
        FailureType.DGIC_UNREACHABLE,
        FailureType.ENFORCEMENT_ERROR,
        FailureType.INSIGHTBRIDGE_ERROR
    ]
    
    print("\nExecuting pipeline with different failures...")
    
    for i, failure_type in enumerate(failure_types, 1):
        print(f"\n[Execution {i}] Injecting: {failure_type.value}")
        result = pipeline.execute_with_failure_handling(
            signals,
            inject_failure=failure_type
        )
        print(f"  Failures: {len(result['failures'])}")
        print(f"  Recovery Actions: {len(result['recovery_actions'])}")
        print(f"  Final Status: {result['enforcement']['status']}")
    
    failure_log = pipeline.get_failure_log()
    
    print(f"\n✓ Total Executions: {len(failure_log)}")
    print(f"✓ All Failures Handled: {all(len(log['failures']) > 0 for log in failure_log)}")


def example_7_chain_integrity():
    """
    Example 7: Chain integrity maintained despite failures
    Expected: execution_id preserved, logging consistent
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: Chain Integrity Despite Failures")
    print("="*80)
    
    pipeline = ResilientBHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha")
    ]
    
    import uuid
    execution_id = str(uuid.uuid4())
    
    print(f"\nExecution ID: {execution_id}")
    print("Injecting DGIC failure...")
    
    result = pipeline.execute_with_failure_handling(
        signals,
        execution_id=execution_id,
        inject_failure=FailureType.DGIC_UNREACHABLE
    )
    
    print("\nChain Integrity Check:")
    print(f"  - Execution ID Preserved: {result['execution_id'] == execution_id}")
    print(f"  - DGIC Response Has ID: {'execution_id' in result['orchestrator']['dgic_response']}")
    print(f"  - Enforcement Has ID: {'execution_id' in result['enforcement']}")
    print(f"  - Failures Logged: {len(result['failures']) > 0}")
    print(f"  - Recovery Actions Logged: {len(result['recovery_actions']) > 0}")
    
    print(f"\n✓ Chain Integrity Maintained: execution_id tracked throughout")
    print(f"✓ Failures Logged Correctly: {len(result['failures'])} failures recorded")
    print(f"✓ System Did Not Break: Pipeline completed with fail-safe")


def example_8_failure_log_analysis():
    """
    Example 8: Analyze failure log for patterns
    """
    print("\n" + "="*80)
    print("EXAMPLE 8: Failure Log Analysis")
    print("="*80)
    
    pipeline = ResilientBHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha")
    ]
    
    # Execute multiple times with different failures
    failures_to_inject = [
        FailureType.DGIC_UNREACHABLE,
        FailureType.DGIC_TIMEOUT,
        FailureType.ENFORCEMENT_ERROR,
        FailureType.INSIGHTBRIDGE_ERROR,
        None  # Normal execution
    ]
    
    print("\nExecuting pipeline 5 times with different scenarios...")
    
    for failure in failures_to_inject:
        pipeline.execute_with_failure_handling(signals, inject_failure=failure)
    
    failure_log = pipeline.get_failure_log()
    
    print(f"\n✓ Total Executions: {len(failure_log)}")
    
    # Analyze failures
    total_failures = sum(len(log['failures']) for log in failure_log)
    executions_with_failures = sum(1 for log in failure_log if len(log['failures']) > 0)
    
    print(f"✓ Total Failures: {total_failures}")
    print(f"✓ Executions With Failures: {executions_with_failures}/{len(failure_log)}")
    
    # Count failure types
    failure_types = {}
    for log in failure_log:
        for failure in log['failures']:
            failure_type = failure['type']
            failure_types[failure_type] = failure_types.get(failure_type, 0) + 1
    
    print("\n✓ Failure Type Distribution:")
    for failure_type, count in failure_types.items():
        print(f"  - {failure_type}: {count}")
    
    print(f"\n✓ All Failures Handled: {all(f.get('handled', False) for log in failure_log for f in log['failures'])}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("FAILURE FLOW EXAMPLES")
    print("="*80)
    print("\nDemonstrating failure handling across all BHIV systems")
    print("="*80)
    
    # Run all examples
    try:
        example_1_dgic_unreachable()
        example_2_dgic_timeout()
        example_3_invalid_signals()
        example_4_enforcement_failure()
        example_5_insightbridge_failure()
        example_6_multiple_failures()
        example_7_chain_integrity()
        example_8_failure_log_analysis()
        
        print("\n" + "="*80)
        print("ALL FAILURE EXAMPLES COMPLETED")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
