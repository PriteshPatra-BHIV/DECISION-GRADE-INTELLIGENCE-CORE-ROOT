from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, Field
from typing import Optional
import hashlib
import time
import uuid

app = FastAPI(title="DGIC Runtime API")

VALID_SIGNAL_TYPES = {"THREAT", "SAFE", "UNKNOWN"}


class Signal(BaseModel):
    id: str
    type: str
    priority: float
    timestamp: int
    source: str
    metadata: Optional[dict] = None

    @field_validator("priority")
    @classmethod
    def priority_must_be_bounded(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError("Signal priority must be between 0.0 and 1.0")
        return v

    @field_validator("type")
    @classmethod
    def type_must_be_valid(cls, v):
        if v not in VALID_SIGNAL_TYPES:
            raise ValueError(f"Signal type must be one of {VALID_SIGNAL_TYPES}")
        return v


class DGICRequest(BaseModel):
    execution_id: str
    timestamp: int
    signals: list[Signal]

    @field_validator("execution_id")
    @classmethod
    def validate_execution_id(cls, v):
        try:
            uuid.UUID(v, version=4)
        except ValueError:
            raise ValueError("execution_id must be a valid UUID v4")
        return v


class DGICResponse(BaseModel):
    execution_id: str
    timestamp: int
    decision: str
    confidence: float
    epistemic_state: str
    collapse_trigger: str
    execution_hash: str
    processing_time_ms: int


def deterministic_reasoning(signals: list[Signal]) -> tuple[str, float, str, str]:
    threat_count = sum(1 for s in signals if s.type == "THREAT")
    safe_count = sum(1 for s in signals if s.type == "SAFE")
    unknown_count = sum(1 for s in signals if s.type == "UNKNOWN")
    
    threat_weight = sum(s.priority for s in signals if s.type == "THREAT")
    safe_weight = sum(s.priority for s in signals if s.type == "SAFE")
    
    total_signals = len(signals)
    
    # Determine epistemic state
    if total_signals < 2:
        epistemic_state = "INSUFFICIENT"
        confidence = 0.3
        decision = "REQUEST_MORE_DATA"
        collapse_trigger = "none"
    elif threat_count > 0 and safe_count > 0 and abs(threat_weight - safe_weight) < 0.3:
        epistemic_state = "CONTRADICTORY"
        confidence = 0.5
        decision = "ESCALATE"
        collapse_trigger = "none"
    elif threat_weight > safe_weight and threat_weight > 0.8:
        epistemic_state = "CERTAIN"
        confidence = min(1.0, threat_weight)
        decision = "ESCALATE"
        collapse_trigger = "dominance"
    elif safe_weight > threat_weight and safe_weight > 0.8:
        epistemic_state = "CERTAIN"
        confidence = min(1.0, safe_weight)
        decision = "PROCEED"
        collapse_trigger = "dominance"
    elif 0.4 <= max(threat_weight, safe_weight) <= 0.8:
        epistemic_state = "AMBIGUOUS"
        confidence = max(threat_weight, safe_weight)
        decision = "HOLD"
        collapse_trigger = "none"
    else:
        epistemic_state = "INSUFFICIENT"
        confidence = 0.3
        decision = "REQUEST_MORE_DATA"
        collapse_trigger = "none"
    
    return decision, round(confidence, 2), epistemic_state, collapse_trigger


@app.post("/dgic/evaluate", response_model=DGICResponse)
def evaluate_dgic(request: DGICRequest):
    start_time = time.time()
    
    if not request.signals:
        raise HTTPException(status_code=400, detail="signals list must not be empty")
    
    if len(request.signals) > 100:
        raise HTTPException(status_code=400, detail="signals list must not exceed 100 elements")
    
    # Validate signal IDs are unique
    signal_ids = [s.id for s in request.signals]
    if len(signal_ids) != len(set(signal_ids)):
        raise HTTPException(status_code=400, detail="signal IDs must be unique")
    
    decision, confidence, epistemic_state, collapse_trigger = deterministic_reasoning(request.signals)
    
    # Calculate execution hash
    sorted_signal_ids = sorted(signal_ids)
    hash_input = f"{request.execution_id}{''.join(sorted_signal_ids)}{decision}{epistemic_state}{confidence}"
    execution_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    processing_time_ms = int((time.time() - start_time) * 1000)
    
    return DGICResponse(
        execution_id=request.execution_id,
        timestamp=int(time.time() * 1000),
        decision=decision,
        confidence=confidence,
        epistemic_state=epistemic_state,
        collapse_trigger=collapse_trigger,
        execution_hash=execution_hash,
        processing_time_ms=processing_time_ms
    )



import json


class DGICTrace(BaseModel):
    execution_id: str
    timestamp: int
    input_signals: list[dict]
    reasoning_trace: list[dict]
    collapse_event: dict
    final_state: dict
    execution_hash: str
    trace_hash: str


def generate_trace(request: DGICRequest, decision: str, confidence: float, 
                   epistemic_state: str, collapse_trigger: str, 
                   execution_hash: str, processing_start: float) -> DGICTrace:
    """
    Generate trace data for InsightBridge.
    Per contract Section 4.1
    """
    
    current_time = int(time.time() * 1000)
    
    # Input signals (simplified for trace)
    input_signals = [
        {
            "id": s.id,
            "type": s.type,
            "priority": s.priority,
            "timestamp": s.timestamp
        }
        for s in request.signals
    ]
    
    # Reasoning trace
    threat_weight = sum(s.priority for s in request.signals if s.type == "THREAT")
    safe_weight = sum(s.priority for s in request.signals if s.type == "SAFE")
    
    reasoning_trace = [
        {
            "step": 1,
            "operation": "signal_aggregation",
            "result": {
                "threat_weight": round(threat_weight, 2),
                "safe_weight": round(safe_weight, 2),
                "total_signals": len(request.signals)
            },
            "timestamp": int((processing_start + 0.01) * 1000)
        },
        {
            "step": 2,
            "operation": "state_computation",
            "result": {
                "state": epistemic_state,
                "confidence": confidence
            },
            "timestamp": int((processing_start + 0.02) * 1000)
        }
    ]
    
    # Collapse event
    collapse_occurred = collapse_trigger != "none"
    collapse_event = {
        "occurred": collapse_occurred,
        "trigger": collapse_trigger,
        "timestamp": int((processing_start + 0.03) * 1000),
        "selected_state": decision if collapse_occurred else None,
        "eliminated_states": [],
        "reason": f"Collapse triggered by {collapse_trigger}" if collapse_occurred else "No collapse threshold reached"
    }
    
    # Final state
    final_state = {
        "decision": decision,
        "confidence": confidence,
        "epistemic_state": epistemic_state
    }
    
    # Build trace object
    trace_obj = {
        "execution_id": request.execution_id,
        "timestamp": current_time,
        "input_signals": input_signals,
        "reasoning_trace": reasoning_trace,
        "collapse_event": collapse_event,
        "final_state": final_state,
        "execution_hash": execution_hash
    }
    
    # Calculate trace hash (per contract Section 4.3)
    trace_json = json.dumps(trace_obj, sort_keys=True, separators=(',', ':'))
    trace_hash = hashlib.sha256(trace_json.encode()).hexdigest()
    
    trace_obj["trace_hash"] = trace_hash
    
    return DGICTrace(**trace_obj)


@app.post("/dgic/trace", response_model=DGICTrace)
def get_trace(request: DGICRequest):
    """
    Generate trace data for InsightBridge.
    This endpoint provides detailed reasoning trace for telemetry and replay verification.
    """
    start_time = time.time()
    
    if not request.signals:
        raise HTTPException(status_code=400, detail="signals list must not be empty")
    
    if len(request.signals) > 100:
        raise HTTPException(status_code=400, detail="signals list must not exceed 100 elements")
    
    # Validate signal IDs are unique
    signal_ids = [s.id for s in request.signals]
    if len(signal_ids) != len(set(signal_ids)):
        raise HTTPException(status_code=400, detail="signal IDs must be unique")
    
    decision, confidence, epistemic_state, collapse_trigger = deterministic_reasoning(request.signals)
    
    # Calculate execution hash
    sorted_signal_ids = sorted(signal_ids)
    hash_input = f"{request.execution_id}{''.join(sorted_signal_ids)}{decision}{epistemic_state}{confidence}"
    execution_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    # Generate trace
    trace = generate_trace(
        request, decision, confidence, epistemic_state, 
        collapse_trigger, execution_hash, start_time
    )
    
    return trace
