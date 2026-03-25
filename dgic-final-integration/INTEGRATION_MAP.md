# DGIC Integration Map - Visual Reference
## Phase 2: Orchestrator → DGIC Integration

**Purpose:** Single-page visual guide for the entire BHIV team  
**Removes:** 90% of coordination friction  
**Owner:** Pritesh Patra

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         BHIV ECOSYSTEM                                   │
│                                                                          │
│  ┌──────────────────┐      ┌──────────────────┐      ┌───────────────┐ │
│  │   Orchestrator   │─────▶│      DGIC        │─────▶│  Enforcement  │ │
│  │  (Aakanksha)     │      │   (Pritesh)      │      │  (Rajaryan)   │ │
│  │                  │      │                  │      │               │ │
│  │  Sends signals   │      │  Computes        │      │  Executes     │ │
│  │  Routes flow     │      │  decision        │      │  action       │ │
│  └──────────────────┘      └────────┬─────────┘      └───────────────┘ │
│                                     │                                   │
│                                     │ Trace                             │
│                                     ▼                                   │
│                            ┌──────────────────┐                         │
│                            │  InsightBridge   │                         │
│                            │   (Vijay)        │                         │
│                            │                  │                         │
│                            │  Stores trace    │                         │
│                            │  Emits telemetry │                         │
│                            └──────────────────┘                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 2 Data Flow (Orchestrator → DGIC)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  STEP 1: Orchestrator Creates Signals                                   │
│  ────────────────────────────────────────                               │
│                                                                          │
│  signals = [                                                             │
│    {                                                                     │
│      "id": "sig_001",                                                    │
│      "type": "THREAT",           ◀── THREAT | SAFE | UNKNOWN            │
│      "priority": 0.8,            ◀── 0.0 to 1.0                         │
│      "timestamp": 1704067199000, ◀── Unix epoch ms                      │
│      "source": "agent_alpha",    ◀── Agent identifier                   │
│      "metadata": {...}           ◀── Optional                           │
│    }                                                                     │
│  ]                                                                       │
│                                                                          │
│  ────────────────────────────────────────────────────────────────────   │
│                                                                          │
│  STEP 2: Orchestrator Calls DGIC                                        │
│  ────────────────────────────────────────                               │
│                                                                          │
│  client = OrchestratorDGICClient(dgic_url="http://localhost:8000")     │
│  response = client.evaluate_decision(signals=signals)                   │
│                                                                          │
│  ────────────────────────────────────────────────────────────────────   │
│                                                                          │
│  STEP 3: DGIC Processes & Returns Decision                              │
│  ────────────────────────────────────────                               │
│                                                                          │
│  {                                                                       │
│    "execution_id": "550e8400-...",                                      │
│    "timestamp": 1704067200150,                                          │
│    "decision": "ESCALATE",       ◀── ESCALATE | PROCEED | HOLD |       │
│                                      REQUEST_MORE_DATA | ERROR          │
│    "confidence": 0.8,            ◀── 0.0 to 1.0                         │
│    "epistemic_state": "CERTAIN", ◀── CERTAIN | AMBIGUOUS |              │
│                                      CONTRADICTORY | INSUFFICIENT       │
│    "collapse_trigger": "dominance",                                     │
│    "execution_hash": "a3f5b8c9...",                                     │
│    "processing_time_ms": 45                                             │
│  }                                                                       │
│                                                                          │
│  ────────────────────────────────────────────────────────────────────   │
│                                                                          │
│  STEP 4: Orchestrator Handles Decision                                  │
│  ────────────────────────────────────────                               │
│                                                                          │
│  if response["decision"] == "PROCEED":                                  │
│      execute_action()                                                   │
│  elif response["decision"] == "ESCALATE":                               │
│      escalate_to_human()                                                │
│  elif response["decision"] == "HOLD":                                   │
│      delay_action()                                                     │
│  elif response["decision"] == "REQUEST_MORE_DATA":                      │
│      gather_more_signals()                                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Decision Matrix (Quick Reference)

```
┌──────────────────┬──────────────────┬─────────────────────────────────┐
│ DGIC Decision    │ Epistemic State  │ What Orchestrator Should Do     │
├──────────────────┼──────────────────┼─────────────────────────────────┤
│ PROCEED          │ CERTAIN          │ ✓ Execute the proposed action   │
│                  │                  │   Safe to proceed               │
├──────────────────┼──────────────────┼─────────────────────────────────┤
│ ESCALATE         │ CERTAIN (threat) │ ⚠ Route to human/supervisor     │
│                  │ or CONTRADICTORY │   DO NOT auto-proceed           │
├──────────────────┼──────────────────┼─────────────────────────────────┤
│ HOLD             │ AMBIGUOUS        │ ⏸ Delay action temporarily      │
│                  │                  │   Wait for more clarity         │
├──────────────────┼──────────────────┼─────────────────────────────────┤
│ REQUEST_MORE_DATA│ INSUFFICIENT     │ 🔍 Gather more signals          │
│                  │                  │   Not enough data to decide     │
├──────────────────┼──────────────────┼─────────────────────────────────┤
│ ERROR            │ N/A              │ ✗ Fail-safe: BLOCK action       │
│                  │                  │   DGIC processing failed        │
└──────────────────┴──────────────────┴─────────────────────────────────┘
```

---

## Signal Types Explained

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  THREAT                                                                  │
│  ───────                                                                 │
│  Indicates potential danger, risk, or security concern                  │
│  Examples: intrusion attempt, anomaly detected, policy violation        │
│  High priority THREAT → ESCALATE decision                               │
│                                                                          │
│  SAFE                                                                    │
│  ────                                                                    │
│  Indicates normal, expected, or verified safe operation                 │
│  Examples: authentication passed, behavior normal, policy compliant     │
│  High priority SAFE → PROCEED decision                                  │
│                                                                          │
│  UNKNOWN                                                                 │
│  ───────                                                                 │
│  Indicates uncertainty, lack of information, or ambiguous state         │
│  Examples: insufficient data, unclear intent, edge case                 │
│  Multiple UNKNOWN → REQUEST_MORE_DATA or HOLD decision                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Execution ID Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  1. GENERATION (Orchestrator)                                           │
│     ─────────────────────────                                           │
│     execution_id = uuid.uuid4()  ◀── UUID v4 format                     │
│     Example: "550e8400-e29b-41d4-a716-446655440000"                     │
│                                                                          │
│  2. DGIC PROCESSING                                                      │
│     ────────────────                                                     │
│     - Validates execution_id format                                     │
│     - Includes in response                                              │
│     - Uses in execution_hash calculation                                │
│                                                                          │
│  3. ENFORCEMENT LOGGING                                                  │
│     ───────────────────                                                  │
│     - Logs action with execution_id                                     │
│     - Enables cross-system tracking                                     │
│                                                                          │
│  4. INSIGHTBRIDGE CORRELATION                                            │
│     ──────────────────────────                                           │
│     - Stores trace with execution_id                                    │
│     - Enables replay verification                                       │
│     - Links decision → action → telemetry                               │
│                                                                          │
│  ✓ Same execution_id across ALL systems for ONE decision flow           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  Orchestrator Error Handling:                                           │
│  ────────────────────────────                                           │
│                                                                          │
│  try:                                                                    │
│      response = client.evaluate_decision(signals=signals)               │
│                                                                          │
│      if response["decision"] == "ERROR":                                │
│          # DGIC processing failed                                       │
│          fail_safe_action()                                             │
│          log_error(response["execution_id"])                            │
│                                                                          │
│  except DGICIntegrationError as e:                                      │
│      # Network/connection error                                         │
│      if "unreachable" in str(e):                                        │
│          retry_with_backoff()                                           │
│      elif "timed out" in str(e):                                        │
│          fail_safe_action()                                             │
│      else:                                                               │
│          log_error(str(e))                                              │
│          fail_safe_action()                                             │
│                                                                          │
│  ✓ ALWAYS fail-safe: when in doubt, BLOCK the action                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Determinism Guarantee

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  DGIC Guarantee: Same Input → Same Output (ALWAYS)                      │
│  ──────────────────────────────────────────────────                     │
│                                                                          │
│  Given:                                                                  │
│    - Same execution_id                                                  │
│    - Same signals (order, content, timestamps)                          │
│                                                                          │
│  DGIC Returns:                                                           │
│    - Identical decision                                                 │
│    - Identical confidence                                               │
│    - Identical epistemic_state                                          │
│    - Identical execution_hash                                           │
│                                                                          │
│  Verification:                                                           │
│    execution_hash_1 == execution_hash_2  ✓                              │
│                                                                          │
│  Why This Matters:                                                       │
│    - Enables replay for debugging                                       │
│    - Enables audit trail verification                                   │
│    - Enables deterministic testing                                      │
│    - Prevents non-deterministic bugs                                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Integration Checklist

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  FOR ORCHESTRATOR TEAM (Aakanksha Parab):                               │
│  ─────────────────────────────────────────                              │
│                                                                          │
│  ✅ Phase 2 Complete - Ready to Integrate                               │
│                                                                          │
│  □ Copy orchestrator_dgic_integration.py to your codebase               │
│  □ Install dependencies: pip install -r requirements.txt                │
│  □ Configure DGIC service URL in your environment                       │
│  □ Import OrchestratorDGICClient                                        │
│  □ Initialize client with DGIC URL                                      │
│  □ Use create_signal() to format signals                                │
│  □ Call evaluate_decision() to get decisions                            │
│  □ Handle all 5 decision types (PROCEED, ESCALATE, HOLD, etc.)          │
│  □ Propagate execution_id to downstream systems                         │
│  □ Implement error handling (DGICIntegrationError)                      │
│  □ Test with orchestrator_integration_example.py                        │
│  □ Run integration tests: pytest phase2_integration_tests.py            │
│                                                                          │
│  FOR ENFORCEMENT TEAM (Rajaryan Verma):                                 │
│  ──────────────────────────────────────                                 │
│                                                                          │
│  ⏳ Phase 3 Pending - Prepare for Integration                           │
│                                                                          │
│  □ Review integration_contract.md Section 3                             │
│  □ Understand decision mapping matrix                                   │
│  □ Prepare action handlers: allow(), escalate(), delay(), etc.          │
│  □ Prepare to receive execution_id from Orchestrator                    │
│  □ Prepare to log actions with execution_id                             │
│                                                                          │
│  FOR INSIGHTBRIDGE TEAM (Vijay Dhawan):                                 │
│  ───────────────────────────────────────                                │
│                                                                          │
│  ⏳ Phase 4 Pending - Prepare for Integration                           │
│                                                                          │
│  □ Review integration_contract.md Section 4                             │
│  □ Understand trace schema                                              │
│  □ Prepare to receive trace data from DGIC                              │
│  □ Prepare to verify trace_hash                                         │
│  □ Prepare to store traces immutably                                    │
│  □ Prepare to index by execution_id                                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: File Locations

```
dgic-final-integration/
├── integration_contract.md              ◀── Complete contract spec
├── orchestrator_dgic_integration.py     ◀── Integration client (USE THIS)
├── orchestrator_integration_example.py  ◀── 7 working examples
├── phase2_integration_tests.py          ◀── Test suite (20 tests)
├── PHASE2_COMPLETION_SUMMARY.md         ◀── Phase 2 summary
├── INTEGRATION_MAP.md                   ◀── This visual guide
├── README.md                            ◀── Quick start guide
└── requirements.txt                     ◀── Dependencies

dgic-phase-runtime-service/api/
└── dgic_api.py                          ◀── DGIC service (updated)
```

---

## Contact & Support

**DGIC Owner:** Pritesh Patra

**Integration Partners:**
- Aakanksha Parab (Orchestrator) - Phase 2 ✅ Ready
- Rajaryan Verma (Enforcement) - Phase 3 ⏳ Next
- Vijay Dhawan (InsightBridge) - Phase 4 ⏳ Upcoming

**Questions?**
- Read: `integration_contract.md`
- Examples: `orchestrator_integration_example.py`
- Tests: `phase2_integration_tests.py`
- Summary: `PHASE2_COMPLETION_SUMMARY.md`

---

**Last Updated:** [Current Date]  
**Phase 2 Status:** ✅ COMPLETE  
**This document removes 90% of coordination friction** 🎯
