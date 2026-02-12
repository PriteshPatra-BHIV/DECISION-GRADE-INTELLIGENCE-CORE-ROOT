# Test: Collapse Logging & Irreversibility

## Purpose

Verify that all certainty-promoting transitions
are logged and preserved immutably.

---

## Test Case 1
Ambiguous → Known (with evidence and justification)

Expected:
- Transition allowed.
- Journal entry created.
- Entry contains:
  - Transition ID
  - Timestamp
  - Previous state
  - Target state
  - Evidence reference
  - Justification
  - Actor

---

## Test Case 2
Ambiguous → Known (without evidence)

Expected:
Blocked.
No journal entry created.

---

## Test Case 3
Inferred → Known (without evidence)

Expected:
Blocked.
No journal entry created.

---

## Test Case 4
Journal Modification Attempt

Simulate:
Manual deletion or modification of prior entry.

Expected:
System flags violation.
Journal must be treated as append-only.

---

## Irreversibility Rule

Once collapse occurs:

- Previous ambiguity must remain auditable.
- Journal entries must never be overwritten.
- Historical uncertainty must remain reconstructable.

---

## Failure Condition

If collapse occurs without journal entry,
system integrity fails.
