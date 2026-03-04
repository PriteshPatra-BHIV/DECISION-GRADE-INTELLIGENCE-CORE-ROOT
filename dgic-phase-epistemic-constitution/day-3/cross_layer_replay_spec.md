# cross_layer_replay_spec.md
# Cross Layer Replay Specification

Replay ensures deterministic reconstruction of epistemic state.

Rules:

• Each envelope includes lineage_hash
• parent_hash links envelopes across layers
• Replay must produce identical epistemic outputs.