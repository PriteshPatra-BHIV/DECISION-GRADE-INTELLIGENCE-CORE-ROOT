# version_mismatch_policy.md
# Version Mismatch Policy

If schema versions mismatch:

• Downstream must reject envelope
• System must fail closed
• No automatic interpretation allowed
• Schema compatibility must be verified before processing