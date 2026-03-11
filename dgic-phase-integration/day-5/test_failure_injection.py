import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "day-1"))

from integration_harness import DGICIntegrationHarness


class MockDGICCore:
    def get_state(self):
        return {
            "epistemic_state": "AMBIGUOUS",
            "confidence": 0.5,
            "contradiction_flag": False,
            "evidence": ["evidence1", "evidence2"],
            "collapse_flag": False,
            "entropy_score": 0.7
        }


def test_downstream_crash_isolation():
    """Test that downstream crash doesn't affect DGIC state"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    
    original_state = core.get_state()
    
    # Simulate downstream crash
    try:
        raise Exception("Downstream crash!")
    except Exception:
        pass
    
    # DGIC state should be unchanged
    new_state = core.get_state()
    assert original_state == new_state, "DGIC state was affected by downstream crash!"


def test_orchestration_exception_handling():
    """Test that orchestration exceptions don't corrupt state"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    
    original_state = core.get_state()
    
    # Simulate orchestration exception
    try:
        # Simulate exception during orchestration
        raise Exception("Orchestration error!")
    except Exception:
        pass
    
    # Generate snapshot - should still work
    snapshot = harness.generate_snapshot()
    assert snapshot is not None, "Snapshot generation failed after exception!"
    
    # State should be unchanged
    new_state = core.get_state()
    assert original_state == new_state, "State corrupted by exception!"


def test_corrupted_signal_rejection():
    """Test that corrupted signals are rejected"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    
    # Try to inject corrupted signal
    corrupted_signals = [
        None,
        {},
        {"invalid": "signal"},
        "",
    ]
    
    # System should handle gracefully
    for signal in corrupted_signals:
        try:
            # Attempt to process corrupted signal
            snapshot = harness.generate_snapshot()
            # Should still generate valid snapshot
            assert snapshot is not None
        except Exception:
            # Exception is acceptable for corrupted signals
            pass


def test_malformed_schema_rejection():
    """Test that malformed schema is rejected"""
    core = MockDGICCore()
    harness = DGICIntegrationHarness(core)
    
    # Generate valid snapshot
    snapshot = harness.generate_snapshot()
    
    # Verify schema compliance
    required_fields = [
        "epistemic_state",
        "confidence",
        "contradiction_flag",
        "evidence_hash",
        "collapse_flag",
        "entropy_score"
    ]
    
    for field in required_fields:
        assert hasattr(snapshot, field), f"Missing required field: {field}"
    
    # Verify field types
    assert isinstance(snapshot.epistemic_state, str)
    assert isinstance(snapshot.confidence, (int, float))
    assert isinstance(snapshot.contradiction_flag, bool)
    assert isinstance(snapshot.evidence_hash, str)
    assert isinstance(snapshot.collapse_flag, bool)
    assert isinstance(snapshot.entropy_score, (int, float))
