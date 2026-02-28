"""
Public API - Decision-Grade Intelligence Core

Minimal public interface for external systems.
All outputs remain non-authoritative.
"""

from typing import List, Dict, Any, Optional
from core.intelligence_core import IntelligenceCore
from learning.policy_suggestion_engine import PolicySuggestionEngine
from learning.bounded_learning_rules import BoundedLearningRules
from learning.supervision_gate import SupervisionGate


class DecisionGradeAPI:
    """
    Public API for Decision-Grade Intelligence Core.
    
    Provides minimal interface for:
    - Signal processing
    - Policy suggestions
    - Supervised learning
    
    All outputs are non-authoritative intelligence only.
    """
    
    def __init__(self):
        self.core = IntelligenceCore()
        self.policy_engine = PolicySuggestionEngine()
        self.learning_rules = BoundedLearningRules()
        self.supervision_gate = SupervisionGate()
    
    def process_signals(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process signals into structured intelligence.
        
        Args:
            signals: List of signal dicts with signal_id, value, source
        
        Returns:
            Intelligence output with uncertainty and non-guarantees
        """
        return self.core.process_signals(signals)
    
    def suggest_policies(
        self,
        context: Dict[str, Any],
        observations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate hypothetical policy suggestions.
        
        Args:
            context: Current context dict
            observations: Historical observations
        
        Returns:
            List of non-binding policy suggestions with uncertainty
        """
        return self.policy_engine.suggest_policies(context, observations)
    
    def request_learning_update(
        self,
        update: Dict[str, Any],
        requester_id: str
    ) -> str:
        """
        Request supervised learning update.
        
        Args:
            update: Update dict with type, value, source
            requester_id: ID of requesting system
        
        Returns:
            Request ID for tracking approval
        """
        return self.supervision_gate.request_approval(update, requester_id)
    
    def approve_learning_update(
        self,
        request_id: str,
        supervisor_id: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Approve pending learning update (supervisor only).
        
        Args:
            request_id: Request ID from request_learning_update
            supervisor_id: ID of approving supervisor
            notes: Optional approval notes
        
        Returns:
            True if approved, False otherwise
        """
        return self.supervision_gate.approve(request_id, supervisor_id, notes)
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status.
        
        Returns:
            Status dict with learning state and pending approvals
        """
        return {
            "learning_enabled": self.learning_rules.learning_enabled,
            "supervision_required": self.learning_rules.supervision_required,
            "pending_approvals": self.supervision_gate.get_pending_count(),
            "refusal_count": self.core.refusal.refusal_count
        }


# Convenience function for quick access
def create_api() -> DecisionGradeAPI:
    """Create and return API instance."""
    return DecisionGradeAPI()
