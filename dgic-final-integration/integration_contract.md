# DGIC Integration Contract v1.0

**Owner:** Pritesh Patra  
**Consumers:** Rajaryan Verma (Enforcement), Aakanksha Parab (Orchestrator), Vijay Dhawan (InsightBridge)  
**Status:** Phase 2 Complete — Orchestrator Integration Implemented  
**Last Updated:** [Current Date]

---

## Phase Completion Status

- ✅ **Phase 1:** Integration Contract Definition — COMPLETE
- ✅ **Phase 2:** Orchestrator → DGIC Integration — COMPLETE
- ⏳ **Phase 3:** DGIC → Enforcement Integration — PENDING
- ⏳ **Phase 4:** DGIC → InsightBridge Integration — PENDING

---

## 1. System Overview

**DGIC Role:**  
Deterministic decision intelligence layer that processes signals and produces epistemic decisions.

**DGIC Does:**
- Accept signals from Orchestrator
- Compute epistemic state deterministically
- Produce decision output for Enforcement
- Emit trace data for InsightBridge

**DGIC Does NOT:**
- Execute actions
- Modify its own past outputs
- Store persistent state across executions
- Make policy decisions

---

## 2. Input Contract (Orchestrator → DGIC)

### 2.1 Endpoint
```
POST /dgic/evaluate
Content-Type: application/json
```

### 2.2 Input Schema
```json
{
  "execution_id": "string (UUID v4, required)",
  "timestamp": "number (Unix epoch ms, required)",
  "signals": [
    {
      "id": "string (required, unique within request)",
      "type": "THREAT | SAFE | UNKNOWN (required)",
      "priority": "number (required, 0.0-1.0)",
      "timestamp": "number (required, Unix epoch ms)",
      "source": "string (required, agent identifier)",
      "metadata": "object (optional)"
    }
  ]
}
```

### 2.3 Field Validation Rules

| Field | Type | Constraints | Error Code |
|-------|------|-------------|------------|
| execution_id | string | UUID v4 format | INPUT_001 |
| timestamp | number | > 0, <= current time + 60s | INPUT_002 |
| signals | array | 1-100 elements | INPUT_003 |
| signals[].id | string | 1-256 chars, unique | INPUT_004 |
| signals[].type | enum | THREAT\|SAFE\|UNKNOWN | INPUT_005 |
| signals[].priority | number | 0.0-1.0 inclusive | INPUT_006 |
| signals[].timestamp | number | > 0, <= request timestamp | INPUT_007 |
| signals[].source | string | 1-128 chars | INPUT_008 |

### 2.4 Input Validation Behavior

**On Invalid Input:**
```json
{
  "status": "ERROR",
  "error_code": "INPUT_XXX",
  "message": "Validation failure description",
  "execution_id": "<original_execution_id>",
  "timestamp": "<current_timestamp>"
}
```

**HTTP Status:** 400 Bad Request

### 2.5 Example Valid Input
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": 1704067200000,
  "signals": [
    {
      "id": "sig_001",
      "type": "THREAT",
      "priority": 0.8,
      "timestamp": 1704067199000,
      "source": "agent_alpha",
      "metadata": {"confidence": 0.9}
    },
    {
      "id": "sig_002",
      "type": "SAFE",
      "priority": 0.6,
      "timestamp": 1704067199500,
      "source": "agent_beta"
    }
  ]
}
```

---

## 3. Output Contract (DGIC → Enforcement)

### 3.1 Output Schema
```json
{
  "execution_id": "string (UUID v4, matches input)",
  "timestamp": "number (Unix epoch ms, processing completion time)",
  "decision": "ESCALATE | PROCEED | HOLD | REQUEST_MORE_DATA | ERROR",
  "confidence": "number (0.0-1.0)",
  "epistemic_state": "CERTAIN | AMBIGUOUS | CONTRADICTORY | INSUFFICIENT",
  "collapse_trigger": "dominance | threshold | timeout | none",
  "execution_hash": "string (SHA-256 hex)",
  "processing_time_ms": "number"
}
```

### 3.2 Decision Mapping Matrix

| Epistemic State | Confidence | Decision | Enforcement Action |
|----------------|------------|----------|--------------------|
| CERTAIN | > 0.8 | PROCEED | allow() |
| CERTAIN | > 0.8 (threat dominant) | ESCALATE | escalate() |
| AMBIGUOUS | 0.4-0.8 | HOLD | delay() |
| CONTRADICTORY | any | ESCALATE | escalate() |
| INSUFFICIENT | < 0.4 | REQUEST_MORE_DATA | request_input() |
| ERROR | 0.0 | ERROR | fail_safe() |

### 3.3 Decision Semantics

**ESCALATE:**  
- Contradictory signals detected OR high-confidence threat
- Requires human/supervisor intervention
- Enforcement MUST NOT auto-proceed

**PROCEED:**  
- High confidence, no contradictions
- Safe to execute action

**HOLD:**  
- Ambiguous state, needs time/data
- Enforcement should delay, not block

**REQUEST_MORE_DATA:**  
- Insufficient signals to decide
- Orchestrator should gather more input

**ERROR:**  
- DGIC processing failure
- Enforcement MUST fail-safe (block action)

### 3.4 Execution Hash Calculation
```
execution_hash = SHA256(
  execution_id + 
  sorted(signal_ids) + 
  decision + 
  epistemic_state + 
  confidence
)
```

### 3.5 Example Output
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": 1704067200150,
  "decision": "HOLD",
  "confidence": 0.65,
  "epistemic_state": "AMBIGUOUS",
  "collapse_trigger": "none",
  "execution_hash": "a3f5b8c9d2e1f4a7b6c5d8e9f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0",
  "processing_time_ms": 45
}
```

---

## 4. Trace Contract (DGIC → InsightBridge)

### 4.1 Trace Schema
```json
{
  "execution_id": "string (UUID v4)",
  "timestamp": "number (Unix epoch ms)",
  "input_signals": [
    {
      "id": "string",
      "type": "string",
      "priority": "number",
      "timestamp": "number"
    }
  ],
  "reasoning_trace": [
    {
      "step": "number",
      "operation": "string",
      "result": "object",
      "timestamp": "number"
    }
  ],
  "collapse_event": {
    "occurred": "boolean",
    "trigger": "string",
    "timestamp": "number",
    "selected_state": "string",
    "eliminated_states": ["string"],
    "reason": "string"
  },
  "final_state": {
    "decision": "string",
    "confidence": "number",
    "epistemic_state": "string"
  },
  "execution_hash": "string (SHA-256 hex)",
  "trace_hash": "string (SHA-256 of entire trace)"
}
```

### 4.2 Trace Immutability Guarantee

**DGIC Guarantees:**
- Trace data is never mutated after emission
- trace_hash verifies complete trace integrity
- execution_hash verifies decision integrity

**InsightBridge MUST:**
- Store trace as-is without modification
- Verify trace_hash on receipt
- Use execution_id for cross-system correlation

### 4.3 Trace Hash Calculation
```
trace_hash = SHA256(JSON.stringify(entire_trace_object))
```

### 4.4 Example Trace
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": 1704067200150,
  "input_signals": [
    {"id": "sig_001", "type": "THREAT", "priority": 0.8, "timestamp": 1704067199000},
    {"id": "sig_002", "type": "SAFE", "priority": 0.6, "timestamp": 1704067199500}
  ],
  "reasoning_trace": [
    {"step": 1, "operation": "signal_aggregation", "result": {"threat_weight": 0.8, "safe_weight": 0.6}, "timestamp": 1704067200010},
    {"step": 2, "operation": "state_computation", "result": {"state": "AMBIGUOUS", "confidence": 0.65}, "timestamp": 1704067200025}
  ],
  "collapse_event": {
    "occurred": false,
    "trigger": "none",
    "timestamp": 1704067200030,
    "selected_state": null,
    "eliminated_states": [],
    "reason": "No collapse threshold reached"
  },
  "final_state": {
    "decision": "HOLD",
    "confidence": 0.65,
    "epistemic_state": "AMBIGUOUS"
  },
  "execution_hash": "a3f5b8c9d2e1f4a7b6c5d8e9f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0",
  "trace_hash": "b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6"
}
```

---

## 5. Execution ID Lifecycle

### 5.1 Generation
- **Owner:** Orchestrator
- **Format:** UUID v4
- **Uniqueness:** Must be unique per request
- **Propagation:** Passed through entire BHIV pipeline

### 5.2 Tracking Flow
```
Orchestrator generates execution_id
    ↓
DGIC receives and validates execution_id
    ↓
DGIC includes execution_id in decision output
    ↓
Enforcement uses execution_id for action logging
    ↓
InsightBridge uses execution_id for trace correlation
```

### 5.3 Replay Requirements

**Given:**
- Same execution_id
- Same input signals (order, content, timestamps)

**DGIC Guarantees:**
- Identical decision output
- Identical execution_hash
- Identical reasoning trace
- Identical trace_hash

**Replay Verification:**
```python
original_hash = dgic_output_1["execution_hash"]
replay_hash = dgic_output_2["execution_hash"]
assert original_hash == replay_hash  # MUST pass
```

---

## 6. Failure Handling Matrix

### 6.1 Input Failures

| Failure Type | DGIC Response | HTTP Status | Enforcement Action |
|--------------|---------------|-------------|--------------------|
| Invalid execution_id | Error response | 400 | Reject request |
| Missing signals | Error response | 400 | Reject request |
| Invalid signal type | Error response | 400 | Reject request |
| Timestamp in future | Error response | 400 | Reject request |
| Empty signals array | Error response | 400 | Reject request |
| Duplicate signal IDs | Error response | 400 | Reject request |

### 6.2 Processing Failures

| Failure Type | DGIC Response | Decision | Enforcement Action |
|--------------|---------------|----------|--------------------|
| Internal error | Error response | ERROR | fail_safe() |
| Timeout | Error response | ERROR | fail_safe() |
| Resource exhaustion | Error response | ERROR | fail_safe() |
| Unexpected exception | Error response | ERROR | fail_safe() |

### 6.3 Error Response Format
```json
{
  "status": "ERROR",
  "error_code": "string",
  "message": "string",
  "execution_id": "string",
  "timestamp": "number",
  "trace_id": "string (for debugging)"
}
```

### 6.4 Downstream Failure Handling

**If Enforcement Fails:**
- DGIC is NOT notified
- Enforcement logs failure with execution_id
- InsightBridge receives enforcement failure trace

**If InsightBridge Fails:**
- DGIC is NOT notified
- Decision execution continues
- Trace data is lost (acceptable)

**If Orchestrator Fails:**
- DGIC never receives request
- No execution_id generated
- System fails before DGIC involvement

---

## 7. Integration Rules (MANDATORY)

### 7.1 Non-Mutation Contract
- **Rule:** No consumer may modify DGIC output
- **Enforcement:** Consumers must treat DGIC output as immutable
- **Verification:** Hash validation on replay

### 7.2 Execution ID Discipline
- **Rule:** All systems use same execution_id for correlation
- **Enforcement:** Logs, traces, actions must reference execution_id
- **Verification:** Cross-system audit by execution_id

### 7.3 Determinism Guarantee
- **Rule:** Same input → same output (always)
- **Enforcement:** DGIC must be stateless and deterministic
- **Verification:** 10,000-run replay test

### 7.4 Fail-Safe Principle
- **Rule:** On error, system defaults to safe state
- **Enforcement:** ERROR decision → block action
- **Verification:** Failure injection tests

### 7.5 No Authority Escalation
- **Rule:** DGIC provides intelligence, not authority
- **Enforcement:** Enforcement owns final action decision
- **Verification:** Enforcement can override DGIC (with logging)

---

## 8. Schema Versioning

### 8.1 Current Version
- **Contract Version:** 1.0
- **Effective Date:** [Current Date]
- **Breaking Changes:** None (initial version)

### 8.2 Version Evolution Rules

**Minor Version (1.x):**
- Add optional fields
- Add new decision types (with backward compatibility)
- Extend metadata

**Major Version (2.0):**
- Remove fields
- Change field types
- Modify decision semantics

### 8.3 Version Negotiation
```json
{
  "contract_version": "1.0",
  "execution_id": "...",
  "signals": [...]
}
```

**If version mismatch:**
- DGIC returns error with supported versions
- Consumer must upgrade or downgrade

---

## 9. Integration Checklist

### For Orchestrator (Aakanksha Parab):
- [ ] Generate UUID v4 for execution_id
- [ ] Validate signals before sending
- [ ] Handle DGIC error responses
- [ ] Implement retry logic (max 3 attempts)
- [ ] Log all requests with execution_id

### For Enforcement (Rajaryan Verma):
- [ ] Implement decision mapping (see 3.2)
- [ ] Handle ERROR decision with fail-safe
- [ ] Log all actions with execution_id
- [ ] Never modify DGIC output
- [ ] Implement override mechanism (with audit)

### For InsightBridge (Vijay Dhawan):
- [ ] Verify trace_hash on receipt
- [ ] Store trace immutably
- [ ] Index by execution_id
- [ ] Never modify trace data
- [ ] Implement trace replay verification

---

## 10. Contact & Coordination

**DGIC Owner:** Pritesh Patra  
**Questions:** [Contact Method]

**Integration Partners:**
- Rajaryan Verma (Enforcement) — [Contact]
- Aakanksha Parab (Orchestrator) — [Contact]
- Vijay Dhawan (InsightBridge) — [Contact]

**Testing Coordinator:** Vinayak Tiwari  
**Functional Testing:** Akash

---

## 11. Phase 2 Implementation Details

### 11.1 Integration Layer

**File:** `orchestrator_dgic_integration.py`

**Provides:**
- `OrchestratorDGICClient` class for calling DGIC
- `create_signal()` helper method for signal creation
- `evaluate_decision()` method for sending signals and receiving decisions
- Full error handling with `DGICIntegrationError`

**Usage Example:**
```python
from orchestrator_dgic_integration import OrchestratorDGICClient

client = OrchestratorDGICClient(dgic_url="http://localhost:8000")

signals = [
    client.create_signal("sig_001", "SAFE", 0.9, "agent_alpha"),
    client.create_signal("sig_002", "SAFE", 0.85, "agent_beta")
]

response = client.evaluate_decision(signals=signals)
print(response["decision"])  # PROCEED
```

### 11.2 Example Scenarios

**File:** `orchestrator_integration_example.py`

**Includes 7 examples:**
1. Normal safe scenario → PROCEED
2. Threat detection → ESCALATE
3. Contradictory signals → ESCALATE
4. Ambiguous scenario → HOLD
5. Insufficient data → REQUEST_MORE_DATA
6. Error handling demonstration
7. Custom execution_id tracking

**Run examples:**
```bash
python orchestrator_integration_example.py
```

### 11.3 Integration Tests

**File:** `phase2_integration_tests.py`

**Test Coverage:**
- Contract compliance (response structure, field validation)
- Signal validation (empty, too many, invalid types)
- Decision mapping (all 5 decision types)
- Determinism (same input → same output)
- Error handling (service unreachable, invalid inputs)

**Run tests:**
```bash
pytest phase2_integration_tests.py -v
```

### 11.4 API Updates

**File:** `dgic-phase-runtime-service/api/dgic_api.py`

**Changes:**
- Updated schema to match integration contract exactly
- Changed signal fields: `signal_id` → `id`, `value` → `priority`
- Changed signal types: `THREAT | SAFE | UNKNOWN` (removed CONTRADICTION, ANOMALY, CORRUPTION)
- Updated response format to include all contract fields
- Added execution_id validation (UUID v4)
- Added signal uniqueness validation
- Implemented execution_hash calculation per contract spec

### 11.5 Function Call Format

**Orchestrator sends:**
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": 1704067200000,
  "signals": [
    {
      "id": "sig_001",
      "type": "THREAT",
      "priority": 0.8,
      "timestamp": 1704067199000,
      "source": "agent_alpha",
      "metadata": {"confidence": 0.9}
    }
  ]
}
```

**DGIC responds:**
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": 1704067200150,
  "decision": "ESCALATE",
  "confidence": 0.8,
  "epistemic_state": "CERTAIN",
  "collapse_trigger": "dominance",
  "execution_hash": "a3f5b8c9d2e1f4a7b6c5d8e9f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0",
  "processing_time_ms": 45
}
```

### 11.6 Integration Checklist for Orchestrator

**For Aakanksha Parab:**
- ✅ Integration client class provided (`OrchestratorDGICClient`)
- ✅ Signal creation helper provided (`create_signal()`)
- ✅ 7 working examples provided
- ✅ Error handling implemented
- ✅ Execution ID generation/validation implemented
- ✅ Integration tests provided (100% coverage)
- ✅ Contract compliance validated

**Next Steps for Orchestrator:**
1. Import `OrchestratorDGICClient` into your codebase
2. Initialize client with DGIC service URL
3. Use `create_signal()` to format signals from your agents
4. Call `evaluate_decision()` to get DGIC decision
5. Handle response based on `decision` field
6. Propagate `execution_id` to downstream systems

---

## 12. Next Steps (Phase 3)

- Implement Orchestrator → DGIC integration
- Provide working code examples
- Test end-to-end flow
- Document actual API calls

---

**Contract Status:** ✅ Phase 2 Complete — Orchestrator Integration Implemented  
**Signature:** Pritesh Patra  
**Date:** [Current Date]

---

## Deliverables Summary

### Phase 1 Deliverables:
- ✅ `integration_contract.md` — Complete contract specification

### Phase 2 Deliverables:
- ✅ `orchestrator_dgic_integration.py` — Integration client class
- ✅ `orchestrator_integration_example.py` — 7 working examples
- ✅ `phase2_integration_tests.py` — Comprehensive test suite
- ✅ Updated `dgic_api.py` — Contract-compliant API
- ✅ Updated `integration_contract.md` — Phase 2 documentation


## 13. Phase 3 Implementation Details

### 13.1 Integration Layer

**File:** `enforcement_dgic_integration.py`

**Provides:**
- `EnforcementDGICClient` class for consuming DGIC decisions
- `map_decision_to_action()` method for decision-to-action mapping
- `execute_action()` method with override support
- Action logging and execution tracking
- `consume_dgic_decision()` convenience function

**Usage Example:**
```python
from enforcement_dgic_integration import EnforcementDGICClient

client = EnforcementDGICClient(enable_override=True)

# Receive DGIC decision
dgic_response = {
    "execution_id": "550e8400-e29b-41d4-a716-446655440000",
    "decision": "PROCEED",
    "confidence": 0.92,
    "epistemic_state": "CERTAIN",
    ...
}

# Map to action
action = client.map_decision_to_action(dgic_response)
# Returns: {action: "allow", execution_id: "...", ...}

# Execute action
result = client.execute_action(action)
# Returns: {status: "ALLOWED", message: "...", ...}
```

### 13.2 Example Scenarios

**File:** `enforcement_integration_example.py`

**Includes 8 examples:**
1. PROCEED → allow() - High confidence safe
2. ESCALATE (Threat) → escalate() - Threat detected
3. ESCALATE (Contradiction) → escalate() - Contradictory signals
4. HOLD → delay() - Ambiguous signals
5. REQUEST_MORE_DATA → request_input() - Insufficient data
6. ERROR → fail_safe() - DGIC failure
7. Override mechanism - Human override
8. Execution tracking - Multi-decision tracking

**Run examples:**
```bash
python enforcement_integration_example.py
```

### 13.3 Integration Tests

**File:** `phase3_integration_tests.py`

**Test Coverage:**
- Decision mapping (7 tests) - All decision types
- Action execution (5 tests) - All action types
- Override mechanism (4 tests) - Override functionality
- Logging and tracking (4 tests) - Execution ID tracking
- Contract compliance (3 tests) - Contract adherence
- Convenience function (2 tests) - Helper function

**Run tests:**
```bash
pytest phase3_integration_tests.py -v
```

### 13.4 Decision-to-Action Mapping

**Implementation per contract Section 3.2:**

| DGIC Decision | Enforcement Action | Status | Description |
|---------------|-------------------|--------|-------------|
| PROCEED | allow() | ALLOWED | Permit operation |
| ESCALATE | escalate() | ESCALATED | Route to human |
| HOLD | delay() | DELAYED | Postpone decision |
| REQUEST_MORE_DATA | request_input() | INPUT_REQUESTED | Request signals |
| ERROR | fail_safe() | BLOCKED | Block operation |

### 13.5 Real Execution Flow

**Complete Flow:**
```
DGIC Decision Output
    ↓
EnforcementDGICClient.map_decision_to_action()
    ↓
Action Result {action, execution_id, ...}
    ↓
EnforcementDGICClient.execute_action()
    ↓
Execution Result {status, message, ...}
    ↓
Enforcement System handles status
```

**Example Flow:**
```python
# 1. DGIC produces decision
dgic_response = {"decision": "PROCEED", "confidence": 0.92, ...}

# 2. Enforcement maps to action
action = client.map_decision_to_action(dgic_response)
# action = {"action": "allow", ...}

# 3. Enforcement executes action
result = client.execute_action(action)
# result = {"status": "ALLOWED", ...}

# 4. Enforcement handles result
if result["status"] == "ALLOWED":
    proceed_with_operation()
```

### 13.6 Override Mechanism

**Purpose:** Allow human operators to override DGIC decisions

**Implementation:**
```python
# DGIC recommends HOLD, operator overrides to allow
action = client.map_decision_to_action(dgic_response)
result = client.execute_action(action, override="allow")

# Override is logged
assert result["override_applied"] == True
```

**Override Rules:**
- Only when `enable_override=True`
- All overrides logged with timestamp
- Original decision preserved
- Valid overrides: allow, escalate, delay, request_input, fail_safe

### 13.7 Execution Tracking

**Logging Types:**
- `ACTION_MAPPING` - Decision → action mapping
- `OVERRIDE` - Override applied
- `EXECUTION` - Action execution result

**Retrieve Logs:**
```python
# Get all logs
all_logs = client.get_action_log()

# Get logs for specific execution
logs = client.get_action_log(execution_id="550e8400-...")
```

### 13.8 Integration Checklist for Enforcement

**For Rajaryan Verma:**
- ✅ Integration client class provided (`EnforcementDGICClient`)
- ✅ Decision-to-action mapping implemented
- ✅ All 5 action types implemented
- ✅ Override mechanism provided
- ✅ Logging and tracking implemented
- ✅ 8 working examples provided
- ✅ Integration tests provided (25 tests)
- ✅ Contract compliance validated

**Next Steps for Enforcement:**
1. Import `EnforcementDGICClient` into your codebase
2. Initialize client with override settings
3. Receive DGIC decisions from API or Orchestrator
4. Call `map_decision_to_action()` to get action
5. Call `execute_action()` to execute (with optional override)
6. Handle execution result based on `status` field
7. Use `get_action_log()` for audit trails

---

## Deliverables Summary (Updated)

### Phase 1 Deliverables:
- ✅ `integration_contract.md` — Complete contract specification

### Phase 2 Deliverables:
- ✅ `orchestrator_dgic_integration.py` — Integration client class
- ✅ `orchestrator_integration_example.py` — 7 working examples
- ✅ `phase2_integration_tests.py` — Comprehensive test suite
- ✅ Updated `dgic_api.py` — Contract-compliant API
- ✅ Updated `integration_contract.md` — Phase 2 documentation

### Phase 3 Deliverables:
- ✅ `enforcement_dgic_integration.py` — Enforcement client class
- ✅ `enforcement_integration_example.py` — 8 working examples
- ✅ `phase3_integration_tests.py` — Comprehensive test suite (25 tests)
- ✅ `PHASE3_COMPLETION_SUMMARY.md` — Handover documentation
- ✅ Updated `integration_contract.md` — Phase 3 documentation

---

**Contract Status:** ✅ Phase 3 Complete — Enforcement Integration Implemented  
**Signature:** Pritesh Patra  
**Date:** [Current Date]
