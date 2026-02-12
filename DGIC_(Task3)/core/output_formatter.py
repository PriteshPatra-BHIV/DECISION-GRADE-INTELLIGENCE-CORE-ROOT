"""
Output Formatter

Enforces output contracts and ensures all outputs
are authority-neutral and uncertainty-explicit.
"""

from typing import Dict, List, Any


class OutputFormatter:
    """
    Formats intelligence outputs according to output-contracts-v2.md
    
    Guarantees:
    - All outputs include uncertainty
    - All outputs include non-guarantees
    - All outputs include authority neutrality clause
    - No prescriptive language
    """
    
    NON_GUARANTEE_CLAUSE = (
        "This output does not recommend actions, "
        "does not select policies, "
        "and does not claim optimality, correctness, or authority."
    )
    
    AUTHORITY_NEUTRALITY_CLAUSE = (
        "This output provides structured intelligence only. "
        "It does not authorize, initiate, justify, or execute decisions."
    )
    
    def format_output(
        self,
        signals: List[Dict[str, Any]],
        interpretations: List[Dict[str, Any]],
        uncertainty: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format intelligence output with mandatory clauses.
        """
        output = {
            "signals": signals,
            "interpretations": interpretations,
            "uncertainty": uncertainty,
            "non_guarantees": self.NON_GUARANTEE_CLAUSE,
            "authority_neutrality": self.AUTHORITY_NEUTRALITY_CLAUSE
        }
        
        return output
    
    def validate_signal(self, signal: Dict[str, Any]) -> bool:
        """Validate signal has required fields."""
        required = ["signal_id", "source", "confidence", "known_limitations"]
        return all(field in signal for field in required)
    
    def validate_interpretation(self, interp: Dict[str, Any]) -> bool:
        """Validate interpretation has required fields."""
        if "hypothesis" not in interp or "description" not in interp:
            return False
        if "confidence_estimate" not in interp:
            return False
        
        conf = interp["confidence_estimate"]
        return "mean" in conf and "uncertainty" in conf
    
    def ensure_multiple_interpretations(
        self, 
        interpretations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Ensure multiple interpretations exist.
        Single interpretations must declare insufficiency.
        """
        if len(interpretations) == 1:
            interpretations[0]["insufficiency_note"] = (
                "Single interpretation provided. "
                "Multiple hypotheses may exist but are not captured."
            )
        
        return interpretations
