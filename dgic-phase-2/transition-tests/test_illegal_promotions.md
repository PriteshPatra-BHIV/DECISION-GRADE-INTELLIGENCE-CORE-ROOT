# Test: Illegal State Promotions

## Purpose

Ensure the transition engine blocks all invalid epistemic promotions.

---

## Test Case 1
Unknown → Known (without new evidence)

Expected:
Blocked.

---

## Test Case 2
Unknown → Inferred (without signal)

Expected:
Blocked.

---

## Test Case 3
Inferred → Known (without new evidence)

Expected:
Blocked.

---

## Test Case 4
Ambiguous → Known (without new evidence)

Expected:
Blocked.

---

## Test Case 5
Ambiguous → Known (with evidence but no justified collapse)

Expected:
Blocked.

---

## Test Case 6
Ambiguous → Known (with new evidence AND justified collapse)

Expected:
Allowed.

---

## Integrity Rule

If any illegal promotion succeeds,
the system fails irreversibility compliance.
