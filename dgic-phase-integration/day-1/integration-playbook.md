# DGIC Integration Playbook

## Purpose
Provide deterministic, immutable integration boundary for downstream layers.

## Architecture Model

DGIC Core → Immutable Snapshot → Integration Schema → Downstream Consumers

## Integration Rules

- Core never exposed directly
- Snapshots are frozen structures
- Serialization is deterministic (sorted keys)
- Evidence must be hashed
- Replay must produce identical output

## Failure Handling

- Fail closed on corruption
- Reject malformed schema
- Never auto-collapse ambiguity

## Replay Discipline

- Same input → Same output
- No hidden randomness
- No time-dependent logic

## Certification Requirement

- 1000 deterministic replays (Day 2)
- 10,000 replay proof (Day 6)
- Concurrency proof (Day 6)