"""
End-to-End Pipeline Examples
Owner: Pritesh Patra

Demonstrates complete BHIV pipeline execution:
Orchestrator → DGIC → Enforcement → InsightBridge
"""

from end_to_end_pipeline import BHIVPipeline
import json
from typing import Optional


def example_1_normal_safe_flow():
    """
    Example 1: Normal safe scenario - complete flow
    Expected: PROCEED → allow() → trace stored
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Normal Safe Flow")
    print("="*80)
    
    pipeline = BHIVPipeline(dgic_url="http://localhost:8000")
    
    # Create signals
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
        pipeline.orchestrator.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
    ]
    
    print("\nInput Signals:")
    for sig in signals:
        print(f"  - {sig['id']}: {sig['type']} (priority: {sig['priority']})")
    
    # Execute pipeline
    result = pipeline.execute_pipeline(signals)
    
    print("\nPipeline Result:")
    print(json.dumps(result, indent=2))
    
    print("\n✓ Pipeline Success:", result['success'])
    print("✓ DGIC Decision:", result['dgic']['decision'])
    print("✓ Enforcement Action:", result['enforcement']['action'])
    print("✓ Enforcement Status:", result['enforcement']['status'])
    print("✓ Trace Stored:", result['insightbridge']['trace_stored'])


def example_2_threat_escalation_flow():
    """
    Example 2: Threat detection - escalation flow
    Expected: ESCALATE → escalate() → trace stored
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Threat Escalation Flow")
    print("="*80)
    
    pipeline = BHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_threat_001", "THREAT", 0.95, "security_agent"),
        pipeline.orchestrator.create_signal("sig_threat_002", "THREAT", 0.90, "anomaly_detector")
    ]
    
    print("\nInput Signals:")
    for sig in signals:
        print(f"  - {sig['id']}: {sig['type']} (priority: {sig['priority']})")
    
    result = pipeline.execute_pipeline(signals)
    
    print("\nPipeline Result:")
    print(json.dumps(result, indent=2))
    
    print("\n✓ Pipeline Success:", result['success'])
    print("✓ DGIC Decision:", result['dgic']['decision'])
    print("✓ Enforcement Action:", result['enforcement']['action'])
    print("✓ Enforcement Status:", result['enforcement']['status'])


def example_3_contradictory_signals_flow():
    """
    Example 3: Contradictory signals - escalation flow
    Expected: ESCALATE → escalate() → trace stored
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Contradictory Signals Flow")
    print("="*80)
    
    pipeline = BHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "THREAT", 0.75, "agent_alpha"),
        pipeline.orchestrator.create_signal("sig_002", "SAFE", 0.70, "agent_beta"),
        pipeline.orchestrator.create_signal("sig_003", "THREAT", 0.65, "agent_gamma")
    ]
    
    print("\nInput Signals (Contradictory):")
    for sig in signals:
        print(f"  - {sig['id']}: {sig['type']} (priority: {sig['priority']})")
    
    result = pipeline.execute_pipeline(signals)
    
    print("\nPipeline Result:")
    print(json.dumps(result, indent=2))
    
    print("\n✓ Pipeline Success:", result['success'])
    print("✓ DGIC Decision:", result['dgic']['decision'])
    print("✓ Epistemic State:", result['dgic']['epistemic_state'])
    print("✓ Enforcement Action:", result['enforcement']['action'])


def example_4_ambiguous_hold_flow():
    """
    Example 4: Ambiguous signals - hold flow
    Expected: HOLD → delay() → trace stored
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Ambiguous Hold Flow")
    print("="*80)
    
    pipeline = BHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.6, "agent_alpha"),
        pipeline.orchestrator.create_signal("sig_002", "UNKNOWN", 0.5, "agent_beta")
    ]
    
    print("\nInput Signals (Ambiguous):")
    for sig in signals:
        print(f"  - {sig['id']}: {sig['type']} (priority: {sig['priority']})")
    
    result = pipeline.execute_pipeline(signals)
    
    print("\nPipeline Result:")
    print(json.dumps(result, indent=2))
    
    print("\n✓ Pipeline Success:", result['success'])
    print("✓ DGIC Decision:", result['dgic']['decision'])
    print("✓ Enforcement Action:", result['enforcement']['action'])
    print("✓ Enforcement Status:", result['enforcement']['status'])


def example_5_override_flow():
    """
    Example 5: Human override in enforcement
    Expected: HOLD → delay() → OVERRIDDEN to allow()
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Enforcement Override Flow")
    print("="*80)
    
    pipeline = BHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.65, "agent_alpha"),
        pipeline.orchestrator.create_signal("sig_002", "UNKNOWN", 0.55, "agent_beta")
    ]
    
    print("\nInput Signals:")
    for sig in signals:
        print(f"  - {sig['id']}: {sig['type']} (priority: {sig['priority']})")
    
    print("\n⚠ Human operator will override HOLD → allow")
    
    result = pipeline.execute_pipeline(
        signals,
        enforcement_override="allow"
    )
    
    print("\nPipeline Result:")
    print(json.dumps(result, indent=2))
    
    print("\n✓ Pipeline Success:", result['success'])
    print("✓ DGIC Decision:", result['dgic']['decision'])
    print("✓ Enforcement Action:", result['enforcement']['action'])
    print("✓ Override Applied:", result['enforcement']['override_applied'])


def example_6_multiple_executions():
    """
    Example 6: Multiple pipeline executions with tracking
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: Multiple Pipeline Executions")
    print("="*80)
    
    pipeline = BHIVPipeline(dgic_url="http://localhost:8000")
    
    # Execute multiple scenarios
    scenarios = [
        {
            "name": "Safe Operation",
            "signals": [
                pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
                pipeline.orchestrator.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
            ]
        },
        {
            "name": "Threat Detection",
            "signals": [
                pipeline.orchestrator.create_signal("sig_003", "THREAT", 0.95, "security_agent")
            ]
        },
        {
            "name": "Ambiguous Case",
            "signals": [
                pipeline.orchestrator.create_signal("sig_004", "SAFE", 0.6, "agent_alpha"),
                pipeline.orchestrator.create_signal("sig_005", "UNKNOWN", 0.5, "agent_beta")
            ]
        }
    ]
    
    print("\nExecuting 3 scenarios...")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n[Scenario {i}] {scenario['name']}")
        result = pipeline.execute_pipeline(scenario['signals'])
        print(f"  Decision: {result['dgic']['decision']}")
        print(f"  Action: {result['enforcement']['action']}")
        print(f"  Status: {result['enforcement']['status']}")
    
    # Get execution log
    log = pipeline.get_execution_log()
    
    print(f"\n✓ Total Executions: {len(log)}")
    print("\nExecution Summary:")
    for i, entry in enumerate(log, 1):
        print(f"  {i}. {entry['execution_id'][:8]}... → {entry['dgic']['decision']} → {entry['enforcement']['status']}")


def example_7_cross_system_correlation():
    """
    Example 7: Cross-system correlation using execution_id
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: Cross-System Correlation")
    print("="*80)
    
    pipeline = BHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
        pipeline.orchestrator.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
    ]
    
    # Execute pipeline
    result = pipeline.execute_pipeline(signals)
    execution_id = result['execution_id']
    
    print(f"\nExecution ID: {execution_id}")
    
    # Retrieve from each system
    print("\n[Orchestrator] Signals sent:")
    print(f"  - Count: {result['orchestrator']['signals_sent']}")
    
    print("\n[DGIC] Decision made:")
    print(f"  - Decision: {result['dgic']['decision']}")
    print(f"  - Confidence: {result['dgic']['confidence']}")
    print(f"  - Execution Hash: {result['dgic']['execution_hash'][:16]}...")
    
    print("\n[Enforcement] Action executed:")
    print(f"  - Action: {result['enforcement']['action']}")
    print(f"  - Status: {result['enforcement']['status']}")
    
    print("\n[InsightBridge] Trace stored:")
    print(f"  - Stored: {result['insightbridge']['trace_stored']}")
    print(f"  - Trace Hash: {result['insightbridge']['trace_hash'][:16]}...")
    
    # Correlate
    correlation = pipeline.insightbridge.correlate_by_execution_id(execution_id)
    
    print("\n[Correlation] All systems aligned:")
    print(f"  - Found: {correlation['found']}")
    print(f"  - Input Signals: {len(correlation['input_signals'])}")
    print(f"  - Final Decision: {correlation['final_decision']}")
    print(f"  - Reasoning Steps: {correlation['reasoning_steps']}")
    
    print(f"\n✓ All systems correlated under execution_id: {execution_id[:16]}...")


def example_8_execution_summary():
    """
    Example 8: Get execution summary for specific execution_id
    """
    print("\n" + "="*80)
    print("EXAMPLE 8: Execution Summary Retrieval")
    print("="*80)
    
    pipeline = BHIVPipeline(dgic_url="http://localhost:8000")
    
    signals = [
        pipeline.orchestrator.create_signal("sig_001", "SAFE", 0.9, "agent_alpha")
    ]
    
    # Execute
    result = pipeline.execute_pipeline(signals)
    execution_id = result['execution_id']
    
    print(f"\nExecution ID: {execution_id}")
    
    # Get summary
    summary = pipeline.get_execution_summary(execution_id)
    
    print("\nExecution Summary:")
    print(json.dumps(summary, indent=2))
    
    print(f"\n✓ Summary retrieved for: {execution_id[:16]}...")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("END-TO-END PIPELINE EXAMPLES")
    print("="*80)
    print("\nDemonstrating complete BHIV pipeline:")
    print("Orchestrator → DGIC → Enforcement → InsightBridge")
    print("\nNote: These examples require DGIC service running at http://localhost:8000")
    print("Start with: cd dgic-phase-runtime-service && uvicorn api.dgic_api:app --reload")
    print("="*80)
    
    # Run all examples
    try:
        example_1_normal_safe_flow()
        example_2_threat_escalation_flow()
        example_3_contradictory_signals_flow()
        example_4_ambiguous_hold_flow()
        example_5_override_flow()
        example_6_multiple_executions()
        example_7_cross_system_correlation()
        example_8_execution_summary()
        
        print("\n" + "="*80)
        print("ALL EXAMPLES COMPLETED")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure DGIC service is running:")
        print("  cd dgic-phase-runtime-service")
        print("  uvicorn api.dgic_api:app --reload")
