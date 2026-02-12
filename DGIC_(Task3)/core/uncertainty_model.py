"""
Uncertainty Model

Tracks, preserves, and decays confidence estimates.
Ensures uncertainty is never silently collapsed.
"""

from typing import Dict, List, Any
import time


class UncertaintyModel:
    """
    Manages uncertainty as a first-class output.
    
    Guarantees:
    - Uncertainty is always explicit
    - Confidence decays over time
    - Ambiguity is preserved
    """
    
    def __init__(self, decay_rate: float = 0.05):
        self.decay_rate = decay_rate
        self.last_update = time.time()
        self.known_unknowns: List[str] = []
        self.ambiguities: List[str] = []
    
    def apply_decay(self, confidence: float) -> float:
        """Apply time-based confidence decay."""
        elapsed = time.time() - self.last_update
        cycles = int(elapsed / 60)  # Decay per minute
        decayed = max(0.0, confidence - (self.decay_rate * cycles))
        return decayed
    
    def add_unknown(self, description: str):
        """Record a known unknown."""
        if description not in self.known_unknowns:
            self.known_unknowns.append(description)
    
    def add_ambiguity(self, description: str):
        """Record an ambiguity or conflict."""
        if description not in self.ambiguities:
            self.ambiguities.append(description)
    
    def get_uncertainty_report(self) -> Dict[str, Any]:
        """Generate explicit uncertainty declaration."""
        return {
            "known_unknowns": self.known_unknowns.copy(),
            "ambiguities": self.ambiguities.copy(),
            "confidence_decay": self.decay_rate
        }
    
    def increase_uncertainty(self, reason: str):
        """Explicitly increase uncertainty (allowed behavior)."""
        self.add_ambiguity(f"Uncertainty increased: {reason}")
    
    def reset(self):
        """Clear uncertainty state (supervised only)."""
        self.known_unknowns.clear()
        self.ambiguities.clear()
        self.last_update = time.time()
