import json
import os
from typing import Dict, Any


def load_schema(version: str = "1.0") -> Dict[str, Any]:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(base_dir, "schema", f"epistemic_envelope_schema_v{version.split('.')[0]}.json")
    with open(schema_path, 'r') as f:
        return json.load(f)


def validate_schema_version(envelope: Dict[str, Any], expected_version: str = "1.0") -> bool:
    return envelope.get("schema_version") == expected_version


def reject_incompatible_schema(envelope: Dict[str, Any]) -> None:
    if not validate_schema_version(envelope):
        raise ValueError(f"Schema version mismatch: {envelope.get('schema_version')} != 1.0")


def validate_against_schema(envelope: Dict[str, Any]) -> bool:
    schema = load_schema()
    required = schema.get("required", [])
    return all(field in envelope for field in required)
