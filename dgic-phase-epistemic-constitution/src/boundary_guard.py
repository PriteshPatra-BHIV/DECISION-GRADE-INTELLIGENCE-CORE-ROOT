from typing import Dict, Any, List


ALLOWED_CAPABILITIES = {"inform", "signal", "bound", "refuse"}
FORBIDDEN_CAPABILITIES = {"execute", "enforce", "escalate_authority"}


def check_authority_escalation(envelope: Dict[str, Any], downstream_action: str) -> bool:
    if downstream_action in FORBIDDEN_CAPABILITIES:
        return True
    if envelope.get("collapse_flag") and downstream_action == "collapse":
        return True
    return False


def validate_source_authority(envelope: Dict[str, Any]) -> bool:
    source = envelope.get("source_module", "")
    if source != "DGIC":
        return False
    return True


def detect_contamination(envelope: Dict[str, Any], modifications: List[str]) -> bool:
    protected_fields = {"epistemic_state", "entropy_score", "contradiction_flag", 
                        "collapse_flag", "evidence_hash", "envelope_hash"}
    return any(field in protected_fields for field in modifications)


def enforce_boundary(envelope: Dict[str, Any]) -> Dict[str, Any]:
    if not validate_source_authority(envelope):
        raise ValueError("Invalid source authority")
    return envelope
