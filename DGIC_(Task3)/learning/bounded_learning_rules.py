"""
Bounded Learning Rules (Enforcement)

Enforces learning constraints to prevent
autonomous updates, self-reinforcement, and feedback loops.
"""

from typing import Dict, Any, Optional


class BoundedLearningRules:
    """
    Enforces bounded learning constraints.
    
    All learning must be:
    - Supervised
    - Explainable
    - Reversible
    - Stoppable
    """
    
    def __init__(self):
        self.learning_enabled = False
        self.supervision_required = True
        self.update_history = []
    
    def enable_learning(self, supervisor_id: str):
        """Enable learning only with supervisor approval."""
        if not supervisor_id:
            raise LearningViolationError("Learning requires supervisor authorization")
        
        self.learning_enabled = True
        self.update_history.append({
            "action": "learning_enabled",
            "supervisor": supervisor_id
        })
    
    def disable_learning(self):
        """Disable learning (always allowed)."""
        self.learning_enabled = False
        self.update_history.append({"action": "learning_disabled"})
    
    def validate_update(
        self, 
        update: Dict[str, Any],
        supervisor_approval: Optional[str] = None
    ) -> bool:
        """
        Validate learning update against bounded rules.
        
        Returns True if update is allowed, False otherwise.
        """
        if not self.learning_enabled:
            return False
        
        if self.supervision_required and not supervisor_approval:
            return False
        
        # Check for self-reinforcement
        if self._is_self_reinforcing(update):
            raise LearningViolationError("Self-reinforcement detected")
        
        # Check for feedback loops
        if self._creates_feedback_loop(update):
            raise LearningViolationError("Feedback loop detected")
        
        return True
    
    def apply_update(
        self,
        update: Dict[str, Any],
        supervisor_approval: str
    ) -> Dict[str, Any]:
        """
        Apply supervised learning update.
        Records update for auditability and rollback.
        """
        if not self.validate_update(update, supervisor_approval):
            raise LearningViolationError("Update validation failed")
        
        # Record update
        update_record = {
            "update": update.copy(),
            "supervisor": supervisor_approval,
            "reversible": True
        }
        self.update_history.append(update_record)
        
        return update_record
    
    def rollback_last_update(self) -> bool:
        """Rollback most recent learning update."""
        if not self.update_history:
            return False
        
        last = self.update_history[-1]
        if last.get("reversible", False):
            self.update_history.pop()
            return True
        
        return False
    
    def _is_self_reinforcing(self, update: Dict[str, Any]) -> bool:
        """Check if update uses own outputs as training signal."""
        # Simplified check: look for self-reference
        return update.get("source") == "self" or update.get("feedback_source") == "internal"
    
    def _creates_feedback_loop(self, update: Dict[str, Any]) -> bool:
        """Check if update creates closed feedback loop."""
        # Simplified check: ensure outcome observation is external
        return update.get("outcome_source") == "self_generated"
    
    def get_audit_trail(self) -> list:
        """Return complete learning update history."""
        return self.update_history.copy()


class LearningViolationError(Exception):
    """Raised when learning rules are violated."""
    pass
