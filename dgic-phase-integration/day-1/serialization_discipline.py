import json
import hashlib


def deterministic_json(data: dict) -> str:
    """
    Ensures sorted-key deterministic serialization.
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def hash_evidence(evidence: dict) -> str:
    """
    Deterministic evidence hashing.
    """
    serialized = deterministic_json(evidence)
    return hashlib.sha256(serialized.encode()).hexdigest()  