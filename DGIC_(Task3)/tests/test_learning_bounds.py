"""
Test Learning Bounds

Proves that learning is bounded, supervised,
and cannot create feedback loops or self-reinforce.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from learning.bounded_learning_rules import BoundedLearningRules, LearningViolationError
from learning.supervision_gate import SupervisionGate
from learning.policy_suggestion_engine import PolicySuggestionEngine


class TestBoundedLearning:
    """Test that learning remains bounded and supervised."""
    
    def test_learning_disabled_by_default(self):
        """Verify learning is disabled by default."""
        rules = BoundedLearningRules()
        
        assert not rules.learning_enabled
        assert rules.supervision_required
    
    def test_learning_requires_supervisor(self):
        """Verify learning cannot be enabled without supervisor."""
        rules = BoundedLearningRules()
        
        with pytest.raises(LearningViolationError):
            rules.enable_learning(None)
    
    def test_updates_require_supervision(self):
        """Verify updates require supervisor approval."""
        rules = BoundedLearningRules()
        rules.enable_learning("supervisor-1")
        
        update = {"type": "confidence_adjustment", "value": 0.1}
        
        # Without approval, should fail
        assert not rules.validate_update(update, supervisor_approval=None)
        
        # With approval, should succeed
        assert rules.validate_update(update, supervisor_approval="supervisor-1")
    
    def test_self_reinforcement_blocked(self):
        """Verify self-reinforcement is detected and blocked."""
        rules = BoundedLearningRules()
        rules.enable_learning("supervisor-1")
        
        # Self-reinforcing update
        update = {"source": "self", "value": 0.5}
        
        with pytest.raises(LearningViolationError):
            rules.validate_update(update, supervisor_approval="supervisor-1")
    
    def test_feedback_loops_blocked(self):
        """Verify feedback loops are detected and blocked."""
        rules = BoundedLearningRules()
        rules.enable_learning("supervisor-1")
        
        # Feedback loop update
        update = {"outcome_source": "self_generated"}
        
        with pytest.raises(LearningViolationError):
            rules.validate_update(update, supervisor_approval="supervisor-1")
    
    def test_updates_are_reversible(self):
        """Verify learning updates can be rolled back."""
        rules = BoundedLearningRules()
        rules.enable_learning("supervisor-1")
        
        update = {"type": "test", "source": "external"}
        rules.apply_update(update, "supervisor-1")
        
        # Should be able to rollback
        assert rules.rollback_last_update()
    
    def test_learning_can_be_disabled(self):
        """Verify learning can be disabled at any time."""
        rules = BoundedLearningRules()
        rules.enable_learning("supervisor-1")
        
        assert rules.learning_enabled
        
        rules.disable_learning()
        
        assert not rules.learning_enabled
    
    def test_audit_trail_maintained(self):
        """Verify all learning updates are recorded."""
        rules = BoundedLearningRules()
        rules.enable_learning("supervisor-1")
        
        update = {"type": "test", "source": "external"}
        rules.apply_update(update, "supervisor-1")
        
        audit_trail = rules.get_audit_trail()
        
        assert len(audit_trail) > 0
        assert any(u.get("action") == "learning_enabled" for u in audit_trail)


class TestSupervisionGate:
    """Test that supervision gate enforces external approval."""
    
    def test_updates_require_approval_request(self):
        """Verify updates must go through approval process."""
        gate = SupervisionGate()
        
        update = {"type": "test"}
        request_id = gate.request_approval(update, "requester-1")
        
        assert request_id is not None
        assert gate.get_pending_count() == 1
    
    def test_approval_requires_supervisor(self):
        """Verify approval requires supervisor ID."""
        gate = SupervisionGate()
        
        request_id = gate.request_approval({"type": "test"}, "requester-1")
        
        # Without supervisor, should fail
        assert not gate.approve(request_id, None)
        
        # With supervisor, should succeed
        assert gate.approve(request_id, "supervisor-1")
    
    def test_rejection_removes_from_pending(self):
        """Verify rejection removes update from pending."""
        gate = SupervisionGate()
        
        request_id = gate.request_approval({"type": "test"}, "requester-1")
        gate.reject(request_id, "supervisor-1", "Not needed")
        
        assert gate.get_pending_count() == 0
    
    def test_approved_updates_retrievable(self):
        """Verify approved updates can be retrieved."""
        gate = SupervisionGate()
        
        update = {"type": "test", "value": 42}
        request_id = gate.request_approval(update, "requester-1")
        gate.approve(request_id, "supervisor-1")
        
        approved = gate.get_approved_update(request_id)
        
        assert approved is not None
        assert approved["update"]["value"] == 42


class TestPolicySuggestionEngine:
    """Test that policy suggestions never execute."""
    
    def test_suggestions_are_hypothetical(self):
        """Verify policy suggestions are marked as hypothetical."""
        engine = PolicySuggestionEngine()
        
        context = {"state": "test"}
        observations = [{"signal_id": "S1"}]
        
        suggestions = engine.suggest_policies(context, observations)
        
        assert len(suggestions) > 0
        assert "non_guarantee" in suggestions[0]
        assert "hypothetical" in suggestions[0]["non_guarantee"].lower()
    
    def test_execution_explicitly_refused(self):
        """Verify execution attempts are refused."""
        engine = PolicySuggestionEngine()
        
        with pytest.raises(RuntimeError):
            engine.refuse_execution()
    
    def test_no_execution_interface(self):
        """Verify engine has no execution methods."""
        engine = PolicySuggestionEngine()
        
        assert not hasattr(engine, "execute_policy")
        assert not hasattr(engine, "apply_policy")
        assert not hasattr(engine, "run_policy")
    
    def test_suggestions_include_uncertainty(self):
        """Verify suggestions include uncertainty estimates."""
        engine = PolicySuggestionEngine()
        
        suggestions = engine.suggest_policies({}, [{"signal_id": "S1"}])
        
        assert "confidence_estimate" in suggestions[0]
        assert "uncertainty" in suggestions[0]["confidence_estimate"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
