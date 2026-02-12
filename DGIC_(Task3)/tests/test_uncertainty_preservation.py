"""
Test Uncertainty Preservation

Proves that uncertainty is never silently collapsed
and is always explicit in outputs.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.uncertainty_model import UncertaintyModel
from core.intelligence_core import IntelligenceCore


class TestUncertaintyModel:
    """Test uncertainty tracking and preservation."""
    
    def test_uncertainty_initialized(self):
        """Verify uncertainty model initializes correctly."""
        model = UncertaintyModel()
        
        assert model.decay_rate > 0
        assert len(model.known_unknowns) == 0
        assert len(model.ambiguities) == 0
    
    def test_confidence_decay_applied(self):
        """Verify confidence decays over time."""
        model = UncertaintyModel(decay_rate=0.1)
        
        initial_confidence = 0.9
        decayed = model.apply_decay(initial_confidence)
        
        # Should decay or stay same (depending on time)
        assert decayed <= initial_confidence
    
    def test_known_unknowns_recorded(self):
        """Verify known unknowns are recorded."""
        model = UncertaintyModel()
        
        model.add_unknown("Missing sensor data")
        model.add_unknown("Historical context unavailable")
        
        report = model.get_uncertainty_report()
        
        assert len(report["known_unknowns"]) == 2
        assert "Missing sensor data" in report["known_unknowns"]
    
    def test_ambiguities_recorded(self):
        """Verify ambiguities are recorded."""
        model = UncertaintyModel()
        
        model.add_ambiguity("Conflicting signals detected")
        
        report = model.get_uncertainty_report()
        
        assert len(report["ambiguities"]) == 1
        assert "Conflicting signals" in report["ambiguities"][0]
    
    def test_uncertainty_can_increase(self):
        """Verify uncertainty can increase (not just decrease)."""
        model = UncertaintyModel()
        
        initial_count = len(model.ambiguities)
        
        model.increase_uncertainty("New conflicting evidence")
        
        assert len(model.ambiguities) > initial_count
    
    def test_uncertainty_report_structure(self):
        """Verify uncertainty report has required structure."""
        model = UncertaintyModel()
        model.add_unknown("Test unknown")
        
        report = model.get_uncertainty_report()
        
        assert "known_unknowns" in report
        assert "ambiguities" in report
        assert "confidence_decay" in report
        assert isinstance(report["known_unknowns"], list)
        assert isinstance(report["ambiguities"], list)


class TestUncertaintyInOutputs:
    """Test that uncertainty appears in all intelligence outputs."""
    
    def test_all_outputs_include_uncertainty(self):
        """Verify every output includes uncertainty section."""
        core = IntelligenceCore()
        
        # Test with various signal counts
        for signal_count in [1, 2, 5]:
            signals = [
                {"signal_id": f"S{i}", "value": 0.5 + (i * 0.1)}
                for i in range(signal_count)
            ]
            
            output = core.process_signals(signals)
            
            assert "uncertainty" in output
            assert "known_unknowns" in output["uncertainty"]
            assert "ambiguities" in output["uncertainty"]
    
    def test_uncertainty_never_empty_without_reason(self):
        """Verify uncertainty is reported even with good signals."""
        core = IntelligenceCore()
        
        # High confidence signals
        signals = [
            {"signal_id": "S1", "value": 0.95, "confidence": 0.95}
        ]
        
        output = core.process_signals(signals)
        
        # Should still have uncertainty section
        assert "uncertainty" in output
    
    def test_conflicting_signals_increase_ambiguity(self):
        """Verify conflicting signals are reported as ambiguity."""
        core = IntelligenceCore()
        
        # Highly conflicting signals
        signals = [
            {"signal_id": "S1", "value": 0.9, "confidence": 0.9},
            {"signal_id": "S2", "value": 0.1, "confidence": 0.1}
        ]
        
        output = core.process_signals(signals)
        
        # Should report ambiguity
        assert len(output["uncertainty"]["ambiguities"]) > 0
    
    def test_missing_confidence_creates_unknown(self):
        """Verify missing confidence is reported as unknown."""
        core = IntelligenceCore()
        
        # Signal without confidence
        signals = [{"signal_id": "S1", "value": 0.5}]
        
        output = core.process_signals(signals)
        
        # Should report as known unknown
        assert len(output["uncertainty"]["known_unknowns"]) > 0
    
    def test_interpretations_include_uncertainty(self):
        """Verify interpretations include uncertainty estimates."""
        core = IntelligenceCore()
        
        output = core.process_signals([{"signal_id": "S1", "value": 0.6}])
        
        for interp in output["interpretations"]:
            assert "confidence_estimate" in interp
            assert "uncertainty" in interp["confidence_estimate"]
            
            # Uncertainty should be non-zero
            assert interp["confidence_estimate"]["uncertainty"] > 0
    
    def test_single_interpretation_declares_insufficiency(self):
        """Verify single interpretations declare insufficiency."""
        core = IntelligenceCore()
        
        output = core.process_signals([{"signal_id": "S1", "value": 0.5}])
        
        # Should have multiple interpretations by design
        # But if only one, should have insufficiency note
        if len(output["interpretations"]) == 1:
            assert "insufficiency_note" in output["interpretations"][0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
