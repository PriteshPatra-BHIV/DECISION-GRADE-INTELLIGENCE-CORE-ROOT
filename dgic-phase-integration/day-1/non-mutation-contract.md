# DGIC Non-Mutation Contract v1

## Core Principle
DGIC internal epistemic state is immutable from all downstream systems.

## Rules

1. Downstream layers (Enforcement, Orchestration, Stress Harness) have read-only access.
2. No downstream system may:
   - Modify epistemic_state
   - Override collapse_flag
   - Adjust entropy_score
   - Inject synthetic confidence
3. Collapse decisions originate strictly within DGIC core.
4. All outputs are serialized snapshots.
5. State references must not be passed — only deep copies or serialized forms.

## Violation Policy
Any detected mutation attempt invalidates integration certification.