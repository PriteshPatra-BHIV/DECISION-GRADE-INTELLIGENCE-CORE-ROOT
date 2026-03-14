import json
import hashlib
from typing import Dict, Any
from jsonschema import validate, ValidationError


class RuntimeSchemaGuard:
    """
    Runtime schema validation guard for DGIC output pipeline.
    Ensures all envelopes conform to integration schema before emission.
    """

    SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": [
            "epistemic_state",
            "confidence",
            "contradiction_flag",
            "evidence_hash",
            "collapse_flag",
            "entropy_score"
        ],
        "properties": {
            "epistemic_state": {
                "type": "string",
                "enum": ["CERTAIN", "AMBIGUOUS", "CONTRADICTORY"]
            },
            "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1
            },
            "contradiction_flag": {
                "type": "boolean"
            },
            "evidence_hash": {
                "type": "string"
            },
            "collapse_flag": {
                "type": "boolean"
            },
            "entropy_score": {
                "type": "number",
                "minimum": 0
            }
        },
        "additionalProperties": False
    }

    @staticmethod
    def validate_envelope(envelope: Dict[str, Any]) -> bool:
        """Validate envelope against schema. Raises ValidationError if invalid."""
        validate(instance=envelope, schema=RuntimeSchemaGuard.SCHEMA)
        return True

    @staticmethod
    def compute_envelope_hash(envelope: Dict[str, Any]) -> str:
        """Compute deterministic hash of envelope for integrity verification."""
        canonical = json.dumps(envelope, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical.encode()).hexdigest()

    @staticmethod
    def verify_envelope_integrity(envelope: Dict[str, Any], expected_hash: str) -> bool:
        """Verify envelope hash matches expected value."""
        computed = RuntimeSchemaGuard.compute_envelope_hash(envelope)
        return computed == expected_hash

    @staticmethod
    def guard_emission(envelope: Dict[str, Any]) -> Dict[str, Any]:
        """
        Guard function: validate and seal envelope before emission.
        Returns sealed envelope with integrity hash.
        """
        RuntimeSchemaGuard.validate_envelope(envelope)
        integrity_hash = RuntimeSchemaGuard.compute_envelope_hash(envelope)
        return {
            "envelope": envelope,
            "integrity_hash": integrity_hash,
            "sealed": True
        }
