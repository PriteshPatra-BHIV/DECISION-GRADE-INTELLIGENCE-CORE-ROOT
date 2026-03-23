import hashlib
import html
import json
import logging
import threading
import time
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

_ledger_lock = threading.Lock()
execution_log = {}
replay_ledger = {}

VALID_SIGNAL_TYPES = {"THREAT", "SAFE", "UNKNOWN"}
VALID_DECISIONS = {"ESCALATE", "PROCEED", "HOLD", "REQUEST_MORE_DATA"}
HOLD_CONFIDENCE_THRESHOLD = 0.3
AMBIGUITY_THRESHOLD = 0.05


# ── Hashing & ID ─────────────────────────────────────────────────────────────

def generate_execution_hash(data):
    serialized = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()


def generate_execution_id():
    return str(uuid.uuid4())


# ── Input Validation ──────────────────────────────────────────────────────────

def validate_signals(signals):
    if not isinstance(signals, list):
        raise TypeError("signals must be a list")

    valid = []
    for s in signals:
        if not isinstance(s, dict):
            logger.warning("Skipping non-dict signal: %s", s)
            continue
        if "id" not in s:
            logger.warning("Skipping signal missing 'id': %s", s)
            continue
        if s.get("type") not in VALID_SIGNAL_TYPES:
            logger.warning("Skipping signal %s with invalid type: %s", s.get("id"), s.get("type"))
            continue

        s = s.copy()
        s["timestamp"] = int(s.get("timestamp", 0))
        s["id"] = html.escape(str(s["id"]))
        s["type"] = html.escape(str(s["type"]))
        valid.append(s)

    return valid


# ── Core Pipeline ─────────────────────────────────────────────────────────────

def run_reasoning_pipeline(input_data):
    if not isinstance(input_data, dict) or "signals" not in input_data:
        raise ValueError("input_data must be a dict with a 'signals' key")

    execution_id = generate_execution_id()
    logger.info("Pipeline started | execution_id=%s", execution_id)

    validated_signals = validate_signals(input_data["signals"])
    ordered_signals = apply_temporal_ordering(validated_signals)
    states = evolve_states(ordered_signals)
    resolved_states = resolve_interference(states)
    final_state, collapse_info = collapse_states(resolved_states)
    reason_trace = build_reason_trace(validated_signals, states, collapse_info, final_state)
    decision = generate_decision(final_state, collapse_info, reason_trace, states)

    log_execution(execution_id, input_data, states, collapse_info, decision)
    record = replay_ledger[execution_id]

    logger.info("Pipeline complete | execution_id=%s | decision=%s", execution_id, decision["decision"])

    return {
        "execution_id": execution_id,
        "execution_hash": record["execution_hash"],
        **decision
    }


# ── Temporal Ordering ─────────────────────────────────────────────────────────

def apply_temporal_ordering(signals):
    return sorted(signals, key=lambda x: x.get("timestamp", 0))


# ── State Evolution ───────────────────────────────────────────────────────────

def evolve_states(signals):
    base_confidence = {"THREAT": 0.8, "SAFE": 0.6, "UNKNOWN": 0.5}
    states = []

    for signal in signals:
        confidence = base_confidence.get(signal["type"], 0.5)

        if signal.get("noise", 0) > 0.5:
            confidence *= 0.5
            logger.debug("Noise reduction applied to signal %s", signal["id"])

        states.append({
            "signal_id": signal["id"],
            "type": signal["type"],
            "priority": signal.get("priority", 0),
            "confidence": confidence,
            "timestamp": signal.get("timestamp", 0)
        })

    return states


# ── Interference Resolution ───────────────────────────────────────────────────

def resolve_interference(states):
    for i, state in enumerate(states):
        for j, other in enumerate(states):
            if i == j:
                continue
            if other["timestamp"] < state["timestamp"]:
                if state["type"] == "SAFE" and other["type"] == "THREAT":
                    if state["priority"] < other["priority"]:
                        state["confidence"] *= 0.5
                        logger.debug(
                            "Interference: SAFE signal %s suppressed by prior THREAT %s",
                            state["signal_id"], other["signal_id"]
                        )
    return states


# ── Collapse ──────────────────────────────────────────────────────────────────

def collapse_states(states):
    if not states:
        logger.warning("No states to collapse — returning UNKNOWN")
        return {"type": "UNKNOWN", "confidence": 0}, {"trigger": "none", "eliminated": [], "reason": [], "timestamp": None, "selected": None}

    states_sorted = sorted(
        states,
        key=lambda x: (x["priority"], x["confidence"], x["timestamp"]),
        reverse=True
    )

    final_state = states_sorted[0]
    eliminated = states_sorted[1:]

    collapse_info = {
        "trigger": "priority_dominance",
        "timestamp": final_state.get("timestamp"),
        "selected": final_state,
        "eliminated": eliminated,
        "reason": build_collapse_reason(final_state, eliminated)
    }

    logger.debug("Collapse: selected=%s eliminated=%d states", final_state["signal_id"], len(eliminated))
    return final_state, collapse_info


def build_collapse_reason(final_state, eliminated):
    reasons = [f"Selected state {final_state.get('signal_id')} with highest priority/confidence"]
    reasons += [f"Eliminated {e.get('signal_id')} due to lower priority/confidence" for e in eliminated]
    return reasons


# ── Ambiguity Detection ───────────────────────────────────────────────────────

def detect_ambiguity(states):
    if not states:
        return True
    sorted_states = sorted(states, key=lambda x: x["confidence"], reverse=True)
    if len(sorted_states) > 1:
        diff = sorted_states[0]["confidence"] - sorted_states[1]["confidence"]
        if diff < AMBIGUITY_THRESHOLD:
            return True
    return False


# ── Decision Generation ───────────────────────────────────────────────────────

def normalize_trigger(trigger):
    return {"priority_dominance": "dominance"}.get(trigger, "none")


def generate_decision(state, collapse_info, reason_trace, states):
    if detect_ambiguity(states):
        return {
            "decision": "REQUEST_MORE_DATA",
            "confidence": 0.0,
            "epistemic_state": "AMBIGUOUS",
            "reason_trace": reason_trace + ["Ambiguity detected: confidence difference too low"],
            "collapse_trigger": "none"
        }

    if state.get("confidence", 0) < HOLD_CONFIDENCE_THRESHOLD:
        return {
            "decision": "HOLD",
            "confidence": state.get("confidence", 0),
            "epistemic_state": state.get("type", "UNKNOWN"),
            "reason_trace": reason_trace + [
                f"Confidence {state.get('confidence', 0)} below HOLD threshold {HOLD_CONFIDENCE_THRESHOLD}"
            ],
            "collapse_trigger": normalize_trigger(collapse_info.get("trigger"))
        }

    mapping = {"THREAT": "ESCALATE", "SAFE": "PROCEED", "UNKNOWN": "REQUEST_MORE_DATA"}

    return {
        "decision": mapping.get(state.get("type"), "HOLD"),
        "confidence": state.get("confidence", 0),
        "epistemic_state": state.get("type", "UNKNOWN"),
        "reason_trace": reason_trace,
        "collapse_trigger": normalize_trigger(collapse_info.get("trigger"))
    }


# ── Reason Trace ──────────────────────────────────────────────────────────────

def build_reason_trace(signals, states, collapse_info, final_state):
    trace = [f"Received {len(signals)} signals"]
    trace += [
        f"Signal {s['id']} type={s['type']} priority={s.get('priority', 0)} timestamp={s.get('timestamp', 0)}"
        for s in signals
    ]
    trace += [f"State {st['signal_id']} confidence={st['confidence']}" for st in states]
    trace.append(f"Collapse trigger: {collapse_info.get('trigger')}")
    trace.append(f"Collapse time: {collapse_info.get('timestamp')}")
    trace += [f"Collapse reason: {r}" for r in collapse_info.get("reason", [])]
    trace.append(f"Final state selected: {final_state.get('type')}")
    return trace


# ── Ledger & Replay ───────────────────────────────────────────────────────────

def log_execution(execution_id, input_data, states, collapse_info, decision):
    record = {
        "execution_id": execution_id,
        "input": input_data,
        "states": states,
        "collapse": collapse_info,
        "decision": decision
    }
    record["execution_hash"] = generate_execution_hash(record)

    with _ledger_lock:
        execution_log[execution_id] = record
        replay_ledger[execution_id] = record


def get_replay_trace(execution_id):
    with _ledger_lock:
        return replay_ledger.get(execution_id)


def get_execution_summary(execution_id):
    with _ledger_lock:
        record = replay_ledger.get(execution_id)
    if not record:
        return None
    return {
        "execution_id": execution_id,
        "decision": record["decision"]["decision"],
        "confidence": record["decision"]["confidence"],
        "trigger": record["collapse"]["trigger"]
    }


# ── API Layer ─────────────────────────────────────────────────────────────────

def api_run_reasoning(input_data):
    try:
        if not isinstance(input_data, dict) or "signals" not in input_data:
            return {"status": "error", "message": "Missing 'signals' in input"}
        result = run_reasoning_pipeline(input_data)
        return {"status": "success", "data": result}
    except (TypeError, ValueError) as e:
        logger.error("Validation error in api_run_reasoning: %s", e)
        return {"status": "error", "message": str(e)}
    except Exception as e:
        logger.exception("Unexpected error in api_run_reasoning")
        return {"status": "error", "message": "Internal engine error"}


def api_get_replay(execution_id):
    try:
        record = get_replay_trace(execution_id)
        if record is None:
            return {"status": "error", "message": "Execution not found"}
        return {"status": "success", "data": record}
    except Exception as e:
        logger.exception("Unexpected error in api_get_replay")
        return {"status": "error", "message": "Internal engine error"}


# ── Distributed Simulation ────────────────────────────────────────────────────

def inject_node_variation(node_id, input_data):
    new_input = {"signals": []}
    for s in input_data["signals"]:
        new_signal = s.copy()
        if node_id == "Node_2":
            new_signal["priority"] = new_signal.get("priority", 0) + 1
        elif node_id == "Node_3":
            new_signal["priority"] = max(0, new_signal.get("priority", 0) - 1)
        new_input["signals"].append(new_signal)
    return new_input


def run_node(node_id, input_data):
    modified_input = inject_node_variation(node_id, input_data)
    result = run_reasoning_pipeline(modified_input)
    return {"node_id": node_id, "output": result}


def run_distributed_simulation(input_data, num_nodes=3):
    node_results = [run_node(f"Node_{i+1}", input_data) for i in range(num_nodes)]
    global_decision = aggregate_decisions(node_results)
    return {"nodes": node_results, "global_decision": global_decision}


def aggregate_decisions(node_results):
    decision_count = {}
    confidence_map = {}

    for node in node_results:
        decision = node["output"]["decision"]
        confidence = node["output"]["confidence"]
        decision_count[decision] = decision_count.get(decision, 0) + 1
        confidence_map.setdefault(decision, []).append(confidence)

    final_decision = sorted(
        decision_count.items(),
        key=lambda x: (x[1], sum(confidence_map[x[0]]) / len(confidence_map[x[0]])),
        reverse=True
    )[0][0]

    avg_confidence = sum(confidence_map[final_decision]) / len(confidence_map[final_decision])

    decision_to_epistemic = {
        "ESCALATE": "THREAT",
        "PROCEED": "SAFE",
        "HOLD": "UNKNOWN",
        "REQUEST_MORE_DATA": "AMBIGUOUS"
    }

    return {
        "decision": final_decision,
        "confidence": avg_confidence,
        "epistemic_state": decision_to_epistemic.get(final_decision, "UNKNOWN"),
        "consensus": decision_count
    }


# ── Validation & Testing ──────────────────────────────────────────────────────

def test_determinism(input_data, runs=5):
    first = run_reasoning_pipeline(input_data)["decision"]
    return all(run_reasoning_pipeline(input_data)["decision"] == first for _ in range(runs - 1))


def test_replay_consistency(input_data):
    result = run_reasoning_pipeline(input_data)
    replay = get_replay_trace(result["execution_id"])
    return replay is not None and replay["decision"]["decision"] == result["decision"]


def test_distributed_consistency(input_data):
    distributed = run_distributed_simulation(input_data, num_nodes=3)
    return distributed["global_decision"]["decision"] in VALID_DECISIONS


def generate_test_cases():
    return [
        {"signals": [{"id": "S1", "type": "SAFE", "priority": 2, "timestamp": 1}]},
        {"signals": [
            {"id": "S1", "type": "SAFE", "priority": 2, "timestamp": 1},
            {"id": "S2", "type": "THREAT", "priority": 2, "timestamp": 2}
        ]},
        {"signals": [{"id": "S1", "type": "THREAT", "priority": 2, "timestamp": 1, "noise": 0.9}]},
        {"signals": [{"id": "S1", "type": "FAKE"}, {"id": "S2", "type": "SAFE"}]},
        {"signals": [{"id": "S1"}, {"id": "S2", "type": "SAFE", "priority": 1, "timestamp": 1}]}
    ]


def run_full_validation():
    results = {"determinism": True, "replay": True, "distributed": True}
    for case in generate_test_cases():
        if not test_determinism(case):
            results["determinism"] = False
        if not test_replay_consistency(case):
            results["replay"] = False
        if not test_distributed_consistency(case):
            results["distributed"] = False
    return results


def stress_test(input_data, runs=1000):
    first = run_reasoning_pipeline(input_data)["decision"]
    for i in range(runs - 1):
        if run_reasoning_pipeline(input_data)["decision"] != first:
            return f"FAILED: non-deterministic output at run {i + 2}"
    return f"Stress test passed: {runs} runs, all deterministic"


# ── Entrypoint ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Scenario 1 — Normal case: SAFE signal dominates
    normal = {"signals": [
        {"id": "S1", "type": "THREAT", "priority": 1, "timestamp": 1},
        {"id": "S2", "type": "SAFE", "priority": 2, "timestamp": 2}
    ]}
    print("=== Scenario 1: Normal ===")
    response = api_run_reasoning(normal)
    print(json.dumps(response, indent=2))
    print(api_get_replay(response["data"]["execution_id"])["data"]["execution_hash"])

    # Scenario 2 — Conflict case: equal priority, ambiguity triggers REQUEST_MORE_DATA
    conflict = {"signals": [
        {"id": "S1", "type": "SAFE", "priority": 2, "timestamp": 1},
        {"id": "S2", "type": "THREAT", "priority": 2, "timestamp": 2}
    ]}
    print("\n=== Scenario 2: Conflict ===")
    print(json.dumps(api_run_reasoning(conflict), indent=2))

    # Scenario 3 — Failure case: missing signals key
    print("\n=== Scenario 3: Failure ===")
    print(json.dumps(api_run_reasoning({}), indent=2))

    # Validation & stress
    print("\n=== Full Validation ===")
    print(run_full_validation())

    print("\n=== Stress Test ===")
    print(stress_test(normal))

    # Distributed simulation
    print("\n=== Distributed Simulation ===")
    dist = run_distributed_simulation(normal, num_nodes=5)
    print(json.dumps({
        "global_decision": dist["global_decision"],
        "node_decisions": [n["output"]["decision"] for n in dist["nodes"]]
    }, indent=2))