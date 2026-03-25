# DGIC Integration Quick Start Guide

## 5-Minute Setup

### Step 1: Clone and Install (1 min)
```bash
git clone <repository-url>
cd CORE-DECISION-INTELLIGENCE
pip install requests fastapi uvicorn pydantic
```

### Step 2: Start DGIC API (1 min)
```bash
cd dgic-phase-runtime-service
uvicorn api.dgic_api:app --host 0.0.0.0 --port 8001
```

### Step 3: Run Your First Integration (3 min)
```python
from dgic_final_integration.end_to_end_pipeline import BHIVPipeline

# Initialize pipeline
pipeline = BHIVPipeline(
    "http://localhost:8000",  # Orchestrator
    "http://localhost:8001",  # DGIC
    "http://localhost:8002",  # Enforcement
    "http://localhost:8003"   # InsightBridge
)

# Execute pipeline
signals = [{"type": "risk", "value": 0.3}]
result = pipeline.execute_pipeline(signals)

print(f"Status: {result['status']}")
print(f"Decision: {result['dgic_decision']}")
print(f"Action: {result['enforcement_action']}")
print(f"Execution ID: {result['execution_id']}")
```

---

## Common Use Cases

### Use Case 1: Low Risk Transaction
```python
signals = [{"type": "risk", "value": 0.2}]
result = pipeline.execute_pipeline(signals)
# Expected: PROCEED → allow
```

### Use Case 2: High Risk Transaction
```python
signals = [{"type": "risk", "value": 0.9}]
result = pipeline.execute_pipeline(signals)
# Expected: ESCALATE → escalate
```

### Use Case 3: Manual Override
```python
from dgic_final_integration.enforcement_dgic_integration import EnforcementDGICClient

enforcement = EnforcementDGICClient("http://localhost:8002")
result = enforcement.execute_action(
    execution_id="550e8400-e29b-41d4-a716-446655440000",
    decision="PROCEED",
    override="escalate",
    override_reason="Manual review required"
)
# Action overridden to escalate
```

### Use Case 4: Replay Execution
```python
from dgic_final_integration.replay_system import ReplaySystem
from dgic_final_integration.insightbridge_dgic_integration import InsightBridgeDGICClient

insightbridge = InsightBridgeDGICClient("http://localhost:8003")
replay_system = ReplaySystem(insightbridge)

replay_result = replay_system.replay_execution(execution_id)
print(f"Replay Status: {replay_result['replay_status']}")
print(f"Timeline Events: {len(replay_result['timeline'])}")
```

### Use Case 5: Audit Trail
```python
audit = replay_system.audit_trail(execution_id)
print(f"Total Events: {audit['summary']['total_events']}")
print(f"Systems: {audit['summary']['systems_involved']}")
```

---

## Decision-Action Quick Reference

| Risk Level | Decision | Action | Description |
|------------|----------|--------|-------------|
| 0.0 - 0.4 | PROCEED | allow | Low risk, allow |
| 0.4 - 0.7 | HOLD | delay | Medium risk, delay |
| 0.7 - 1.0 | ESCALATE | escalate | High risk, escalate |

---

## Testing Quick Reference

### Run All Tests
```bash
cd dgic-final-integration
python -m unittest discover -s . -p "phase*_integration_tests.py"
```

### Run Specific Phase
```bash
python phase8_integration_tests.py
```

### Run Examples
```bash
python orchestrator_examples.py
python enforcement_examples.py
python end_to_end_examples.py
```

---

## Troubleshooting Quick Fixes

### Problem: Connection Refused
```bash
# Check if DGIC API is running
curl http://localhost:8001/health

# Start DGIC API
cd dgic-phase-runtime-service
uvicorn api.dgic_api:app --port 8001
```

### Problem: Import Errors
```bash
# Add to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/CORE-DECISION-INTELLIGENCE"
```

### Problem: Test Failures
```bash
# Enable debug logging
python -m unittest phase8_integration_tests.py -v
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `end_to_end_pipeline.py` | Main pipeline orchestration |
| `failure_flow_pipeline.py` | Failure handling |
| `replay_system.py` | Replay and audit |
| `integration_contract.md` | Complete contract specification |
| `HANDOVER_PACKET.md` | Full documentation |

---

## Next Steps

1. ✓ Read `HANDOVER_PACKET.md` for complete documentation
2. ✓ Review `integration_contract.md` for contract details
3. ✓ Run `phase8_integration_tests.py` to verify setup
4. ✓ Explore `*_examples.py` files for working code
5. ✓ Check `PHASE*_COMPLETION_SUMMARY.md` for phase details

---

## Support

- **Documentation:** `HANDOVER_PACKET.md`
- **Contract:** `integration_contract.md`
- **Examples:** `*_examples.py` files
- **Tests:** `phase*_integration_tests.py` files

**Ready to integrate? Start with `end_to_end_pipeline.py`!**
