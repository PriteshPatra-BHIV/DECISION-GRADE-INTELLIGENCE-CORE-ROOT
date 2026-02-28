"""
Intelligence Core

Main intelligence processing engine that produces
structured truth with explicit uncertainty.

Never makes decisions. Never claims authority.
"""

from typing import List, Dict, Any
from .uncertainty_model import UncertaintyModel
from .refusal_layer import RefusalLayer, AuthorityViolationError
from .output_formatter import OutputFormatter


class IntelligenceCore:
    """
    Decision-Grade Intelligence Core
    
    Produces structured intelligence with explicit uncertainty.
    Refuses all authority, execution, and decision requests.
    """
    
    def __init__(self):
        self.uncertainty = UncertaintyModel()
        self.refusal = RefusalLayer()
        self.formatter = OutputFormatter()
    
    def process_signals(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process signals into structured intelligence output.
        
        Args:
            signals: List of signal dictionaries with signal_id, value, source
        
        Returns:
            Structured intelligence output conforming to contracts
        """
        # Validate and enrich signals
        enriched_signals = []
        for signal in signals:
            enriched = self._enrich_signal(signal)
            if self.formatter.validate_signal(enriched):
                enriched_signals.append(enriched)
        
        # Generate multiple interpretations
        interpretations = self._generate_interpretations(enriched_signals)
        interpretations = self.formatter.ensure_multiple_interpretations(interpretations)
        
        # Get uncertainty report
        uncertainty_report = self.uncertainty.get_uncertainty_report()
        
        # Format output with mandatory clauses
        output = self.formatter.format_output(
            enriched_signals,
            interpretations,
            uncertainty_report
        )
        
        # Validate output doesn't violate authority boundaries
        if not self.refusal.validate_output(output):
            self.refusal.refuse("Output contains authority-claiming language")
        
        return output
    
    def _enrich_signal(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Add required fields to signal."""
        enriched = signal.copy()
        
        if "signal_id" not in enriched:
            enriched["signal_id"] = f"S-{id(signal)}"
        
        if "source" not in enriched:
            enriched["source"] = "unknown"
        
        if "confidence" not in enriched:
            enriched["confidence"] = 0.5
            self.uncertainty.add_unknown("Signal confidence not provided")
        
        if "known_limitations" not in enriched:
            enriched["known_limitations"] = "Limitations not specified"
        
        # Apply confidence decay
        enriched["confidence"] = self.uncertainty.apply_decay(enriched["confidence"])
        
        return enriched
    
    def _generate_interpretations(
        self, 
        signals: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple interpretations from signals.
        Always produces at least 2 hypotheses when possible.
        """
        if not signals:
            return [{
                "hypothesis": "H-INSUFFICIENT",
                "description": "No signals available for interpretation",
                "confidence_estimate": {"mean": 0.0, "uncertainty": 1.0}
            }]
        
        interpretations = []
        
        # Primary interpretation
        avg_confidence = sum(s.get("confidence", 0.5) for s in signals) / len(signals)
        interpretations.append({
            "hypothesis": "H-PRIMARY",
            "description": f"Pattern consistent with {len(signals)} signal(s)",
            "confidence_estimate": {
                "mean": avg_confidence,
                "uncertainty": 0.2
            }
        })
        
        # Alternative interpretation (preserve ambiguity)
        interpretations.append({
            "hypothesis": "H-ALTERNATIVE",
            "description": "Alternative pattern or noise",
            "confidence_estimate": {
                "mean": 1.0 - avg_confidence,
                "uncertainty": 0.3
            }
        })
        
        # Check for conflicts
        if len(signals) > 1:
            confidences = [s.get("confidence", 0.5) for s in signals]
            if max(confidences) - min(confidences) > 0.3:
                self.uncertainty.add_ambiguity(
                    f"Signal confidence varies significantly: {min(confidences):.2f} to {max(confidences):.2f}"
                )
        
        # Validate interpretations
        for interp in interpretations:
            if not self.formatter.validate_interpretation(interp):
                interpretations = [{
                    "hypothesis": "H-INVALID",
                    "description": "Interpretation validation failed",
                    "confidence_estimate": {"mean": 0.0, "uncertainty": 1.0}
                }]
                break
        
        return interpretations
    
    def refuse_decision(self):
        """Explicit refusal if asked to make a decision."""
        self.refusal.refuse("Decision-making requested but not permitted")
    
    def refuse_execution(self):
        """Explicit refusal if asked to execute action."""
        self.refusal.refuse("Action execution requested but not permitted")
    
    def refuse_optimization(self):
        """Explicit refusal if asked to optimize."""
        self.refusal.refuse("Optimization requested but not permitted")
