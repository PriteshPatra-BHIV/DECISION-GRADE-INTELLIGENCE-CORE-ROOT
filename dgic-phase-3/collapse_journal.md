# Collapse Journal Specification

## Purpose

The Collapse Journal is an append-only, cryptographically chained
record of all epistemic state transitions.

It provides:

- Irreversibility
- Auditability
- Deterministic replay integrity

Documentation alone is insufficient.
Runtime enforcement is required.

---

## Journal Structure

Each entry must contain:

- transition_id
- timestamp
- previous_state
- target_state
- new_evidence (boolean)
- justified_collapse (boolean)
- previous_hash
- event_hash

No field may be omitted.

---

## Hash Chain Design

Each event is hashed using:

SHA-256(event_data_without_event_hash)

event_hash is appended to the event.

The next event includes:

previous_hash = prior event_hash

This creates a linked hash chain.

---

## Genesis Entry

The first transition uses:

previous_hash = "GENESIS"

This anchors the journal.

---

## Integrity Guarantees

If any journal entry is:

- Modified
- Reordered
- Deleted

Then:

- Hash chain breaks
- Replay fails
- Integrity violation is detected

---

## Append-Only Requirement

The journal must:

- Only append entries
- Never overwrite prior entries
- Never delete prior entries

Any mutation invalidates determinism.

---

## Collapse Enforcement Rule

If target_state == "Known" AND
(previous_state == "Inferred" OR previous_state == "Ambiguous")

Then:

- new_evidence must be True
- justified_collapse must be True (for Ambiguous → Known)
- Journal entry must be created

Collapse without logging is invalid.

---

## Deterministic Replay Compatibility

Replay engine must:

- Recompute hashes
- Validate hash chain continuity
- Reconstruct identical state sequence

Journal is the source of replay truth.

---

## System Sealing Principle

The Collapse Journal ensures:

- No silent state mutation
- No hidden certainty promotion
- No retroactive epistemic rewriting

Irreversibility is enforced in code.
