# schema_versioning_rules.md
# Schema Versioning Rules

1. Schema version must follow semantic versioning.
2. Minor updates must remain backward compatible.
3. Major version changes require downstream validation.
4. Unknown schema versions must be rejected.
5. Envelope must include schema_version field.