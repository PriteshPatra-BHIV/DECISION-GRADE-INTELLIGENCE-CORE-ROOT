# Collapse Ledger — Irreversibility Encoding

## Purpose

The Collapse Ledger records all certainty-producing transitions.

Collapse must be:

- Explicit
- Evidence-bound
- Logged
- Irreversible
- Replay-verifiable

---

## Collapse Definition

Collapse occurs when:

Ambiguous → Known

OR

Inferred → Known (with new evidence)

---

## Collapse Requirements

For any collapse event:

- new_evidence must be True
- Evidence reference must exist
- Event must be appended to ledger
- Hash must chain to previous entry
- Pre-collapse ambiguity must remain reconstructable

---

## Irreversibility Rule

Once collapse occurs:

- It cannot be undone.
- It cannot be deleted.
- It cannot be rewritten.
- It cannot be silently downgraded.

Collapse is forward-only.

---

## Ambiguity Preservation Rule

Collapse reduces runtime ambiguity
but never erases historical ambiguity.

Ambiguity must remain replay-visible.

---

## Ledger Integrity Guarantee

If:

- A collapse entry is modified
- A collapse entry is removed
- A collapse entry is reordered

Replay must fail.

---

## Seal Statement

Collapse is now a cryptographically irreversible event.
