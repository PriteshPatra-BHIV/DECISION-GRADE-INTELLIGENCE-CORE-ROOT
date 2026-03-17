from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import NamedTuple
import hashlib

app = FastAPI(title="DGIC Runtime API")

VALID_SIGNAL_TYPES = {"THREAT", "CONTRADICTION", "ANOMALY", "CORRUPTION"}


class Signal(BaseModel):
    signal_id: str
    type: str
    value: float

    @field_validator("value")
    @classmethod
    def value_must_be_bounded(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError("Signal value must be between 0.0 and 1.0")
        return v

    @field_validator("type")
    @classmethod
    def type_must_be_valid(cls, v):
        if v not in VALID_SIGNAL_TYPES:
            raise ValueError(f"Signal type must be one of {VALID_SIGNAL_TYPES}")
        return v


class DGICRequest(BaseModel):
    signals: list[Signal]
    context: dict | None = None
    source_system: str
    prior_state: dict | None = None


class DGICResponse(BaseModel):
    epistemic_state: str
    confidence: float
    contradiction_flag: bool
    entropy_score: float
    collapse_flag: bool
    trace_hash: str


class ReasoningResult(NamedTuple):
    state: str
    confidence: float
    contradiction: bool
    entropy: float
    collapse: bool


def deterministic_reasoning(signals, prior_state: dict | None = None) -> ReasoningResult:
    threat_score = 0.0
    anomaly_score = 0.0
    contradiction = False

    for s in signals:
        if s.type == "THREAT":
            threat_score += s.value
        elif s.type == "ANOMALY" or s.type == "CORRUPTION":
            anomaly_score += s.value
        elif s.type == "CONTRADICTION":
            contradiction = True

    # prior_state entropy carries forward if present
    prior_entropy = 0.0
    if prior_state and "entropy_score" in prior_state:
        try:
            prior_entropy = float(prior_state["entropy_score"])
        except (TypeError, ValueError):
            prior_entropy = 0.0

    combined_score = min(1.0, threat_score + anomaly_score * 0.5)
    confidence = round(combined_score, 10)
    entropy = round(max(0.0, (1.0 - confidence + prior_entropy * 0.1)), 10)
    collapse = confidence > 0.85
    state = "CERTAIN" if collapse else "AMBIGUOUS"

    return ReasoningResult(
        state=state,
        confidence=confidence,
        contradiction=contradiction,
        entropy=entropy,
        collapse=collapse,
    )


@app.post("/dgic/evaluate", response_model=DGICResponse)
def evaluate_dgic(request: DGICRequest):
    if not request.signals:
        raise HTTPException(status_code=422, detail="signals list must not be empty")

    result = deterministic_reasoning(request.signals, request.prior_state)

    trace_string = f"{result.state}-{result.confidence}-{result.entropy}-{result.contradiction}"
    trace_hash = hashlib.sha256(trace_string.encode()).hexdigest()

    return DGICResponse(
        epistemic_state=result.state,
        confidence=result.confidence,
        contradiction_flag=result.contradiction,
        entropy_score=result.entropy,
        collapse_flag=result.collapse,
        trace_hash=trace_hash,
    )