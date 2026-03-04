import hashlib
import json
import time
from typing import Dict, Any, Optional


def deterministic_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def compute_hash(envelope: Dict[str, Any]) -> str:
    envelope_copy = {k: v for k, v in envelope.items() if k != "envelope_hash"}
    serialized = deterministic_json(envelope_copy)
    return hashlib.sha256(serialized.encode()).hexdigest()


def create_envelope(
    epistemic_state: str,
    entropy_score: float,
    contradiction_flag: bool,
    collapse_flag: bool,
    evidence_hash: str,
    lineage_hash: str = "GENESIS",
    source_module: str = "DGIC"
) -> Dict[str, Any]:
    envelope = {
        "epistemic_state": epistemic_state,
        "entropy_score": entropy_score,
        "contradiction_flag": contradiction_flag,
        "collapse_flag": collapse_flag,
        "evidence_hash": evidence_hash,
        "lineage_hash": lineage_hash,
        "source_module": source_module,
        "schema_version": "1.0",
        "timestamp": int(time.time())
    }
    envelope["envelope_hash"] = compute_hash(envelope)
    return envelope


def validate_envelope(envelope: Dict[str, Any]) -> bool:
    required = ["epistemic_state", "entropy_score", "contradiction_flag", 
                "collapse_flag", "evidence_hash", "lineage_hash", 
                "source_module", "schema_version", "timestamp", "envelope_hash"]
    if not all(k in envelope for k in required):
        return False
    expected_hash = compute_hash(envelope)
    return expected_hash == envelope["envelope_hash"]


def detect_mutation(envelope: Dict[str, Any]) -> bool:
    return not validate_envelope(envelope)
