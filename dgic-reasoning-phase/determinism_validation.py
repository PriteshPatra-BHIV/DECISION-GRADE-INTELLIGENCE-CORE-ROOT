"""Determinism validation - proves replay stability across multiple runs."""

from multi_state_model import EpistemicState, EpistemicStateSet
from state_evolution_engine import StateEvolutionEngine
from state_interference_model import StateInterferenceModel
from collapse_policy_engine import CollapsePolicyEngine
from knowledge_propagation_model import KnowledgePropagationModel
import json


def run_reasoning_pipeline():
    """Execute complete reasoning pipeline and return deterministic output."""
    
    # Initial hypotheses
    threat_state = EpistemicState(
        epistemic_state="THREAT",
        confidence=0.6,
        entropy=0.4,
        evidence_set=["S1"]
    )
    
    sensor_state = EpistemicState(
        epistemic_state="SENSOR_ERROR",
        confidence=0.3,
        entropy=0.7,
        evidence_set=["S2"]
    )
    
    state_set = EpistemicStateSet()
    state_set.add_state(threat_state)
    state_set.add_state(sensor_state)
    
    output = {"steps": []}
    output["steps"].append({
        "step": "initial",
        "states": state_set.to_list()
    })
    
    # Step 1: Evolution
    evolution_engine = StateEvolutionEngine()
    new_signal = {"signal_id": "S3", "type": "THREAT"}
    state_set = evolution_engine.evolve_states(state_set, new_signal)
    
    output["steps"].append({
        "step": "evolution",
        "states": state_set.to_list()
    })
    
    # Step 2: Interference
    interference_model = StateInterferenceModel()
    state_set = interference_model.apply_interference(state_set)
    
    output["steps"].append({
        "step": "interference",
        "states": state_set.to_list()
    })
    
    # Step 3: Collapse evaluation
    collapse_engine = CollapsePolicyEngine()
    collapse_result = collapse_engine.evaluate_collapse(state_set)
    
    output["steps"].append({
        "step": "collapse",
        "collapsed": collapse_result.to_dict() if collapse_result else None
    })
    
    # Step 4: Knowledge propagation
    node1_states = EpistemicStateSet()
    node1_states.add_state(EpistemicState("THREAT", 0.75, 0.25, ["S1", "S3"]))
    
    node2_states = EpistemicStateSet()
    node2_states.add_state(EpistemicState("THREAT", 0.65, 0.35, ["S2"]))
    
    propagation_model = KnowledgePropagationModel()
    global_state = propagation_model.propagate([node1_states, node2_states])
    
    output["steps"].append({
        "step": "propagation",
        "states": global_state.to_list()
    })
    
    return output


def validate_determinism(num_runs: int = 100) -> bool:
    """Validate that pipeline produces identical output across multiple runs."""
    
    print(f"\n{'='*60}")
    print(f"DETERMINISM VALIDATION TEST")
    print(f"Running pipeline {num_runs} times...")
    print(f"{'='*60}\n")
    
    results = []
    
    for i in range(num_runs):
        output = run_reasoning_pipeline()
        results.append(json.dumps(output, sort_keys=True))
        
        if (i + 1) % 10 == 0:
            print(f"✓ Completed {i + 1}/{num_runs} runs")
    
    # Check all results are identical
    first_result = results[0]
    all_identical = all(r == first_result for r in results)
    
    print(f"\n{'='*60}")
    if all_identical:
        print(f"✓ DETERMINISM VALIDATED")
        print(f"✓ All {num_runs} runs produced identical output")
        print(f"✓ System is replay-stable and deterministic")
    else:
        print(f"✗ DETERMINISM FAILED")
        print(f"✗ Outputs differ across runs")
        for i, result in enumerate(results):
            if result != first_result:
                print(f"  Run {i+1} differs from run 1")
                break
    print(f"{'='*60}\n")
    
    return all_identical


def validate_output_structure(output: dict) -> bool:
    """Validate that output has correct structure."""
    
    if "steps" not in output:
        return False
    
    required_steps = ["initial", "evolution", "interference", "collapse", "propagation"]
    actual_steps = [step["step"] for step in output["steps"]]
    
    return actual_steps == required_steps


if __name__ == "__main__":
    # Run single pipeline to show output
    print("\n" + "="*60)
    print("SINGLE PIPELINE EXECUTION")
    print("="*60 + "\n")
    
    output = run_reasoning_pipeline()
    
    for step in output["steps"]:
        print(f"\nStep: {step['step'].upper()}")
        print("-" * 40)
        if "states" in step:
            for state in step["states"]:
                print(f"  {state['epistemic_state']}: confidence={state['confidence']:.2f}, entropy={state['entropy']:.2f}")
        elif "collapsed" in step:
            if step["collapsed"]:
                print(f"  Collapsed to: {step['collapsed']['epistemic_state']}")
            else:
                print(f"  No collapse - ambiguity preserved")
    
    # Validate structure
    if validate_output_structure(output):
        print("\n✓ Output structure is valid")
    else:
        print("\n✗ Output structure is invalid")
    
    # Run determinism validation
    is_deterministic = validate_determinism(num_runs=100)
    
    if is_deterministic:
        print("\n✓ PRODUCTION READY: System is deterministic and replay-stable")
    else:
        print("\n✗ PRODUCTION ISSUE: System is not deterministic")
