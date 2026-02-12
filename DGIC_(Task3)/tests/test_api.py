"""
Test Public API

Verifies the public API maintains all guarantees.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import DecisionGradeAPI, create_api


class TestPublicAPI:
    """Test public API interface."""
    
    def test_api_creation(self):
        """Verify API can be created."""
        api = create_api()
        assert api is not None
        assert isinstance(api, DecisionGradeAPI)
    
    def test_process_signals_via_api(self):
        """Verify signal processing through API."""
        api = create_api()
        
        signals = [{"signal_id": "S1", "value": 0.7, "source": "test"}]
        output = api.process_signals(signals)
        
        assert "interpretations" in output
        assert "uncertainty" in output
        assert "non_guarantees" in output
        assert "authority_neutrality" in output
    
    def test_suggest_policies_via_api(self):
        """Verify policy suggestions through API."""
        api = create_api()
        
        context = {"state": "test"}
        observations = [{"signal_id": "S1"}]
        
        suggestions = api.suggest_policies(context, observations)
        
        assert len(suggestions) > 0
        assert "non_guarantee" in suggestions[0]
    
    def test_learning_workflow_via_api(self):
        """Verify supervised learning workflow through API."""
        api = create_api()
        
        # Request update
        update = {"type": "test", "value": 0.5, "source": "external"}
        request_id = api.request_learning_update(update, "requester-1")
        
        assert request_id is not None
        
        # Check status
        status = api.get_system_status()
        assert status["pending_approvals"] == 1
        
        # Approve update
        approved = api.approve_learning_update(request_id, "supervisor-1")
        assert approved
        
        # Verify pending cleared
        status = api.get_system_status()
        assert status["pending_approvals"] == 0
    
    def test_system_status_via_api(self):
        """Verify system status reporting."""
        api = create_api()
        
        status = api.get_system_status()
        
        assert "learning_enabled" in status
        assert "supervision_required" in status
        assert "pending_approvals" in status
        assert "refusal_count" in status
    
    def test_api_maintains_authority_boundaries(self):
        """Verify API outputs maintain authority boundaries."""
        api = create_api()
        
        output = api.process_signals([{"signal_id": "S1", "value": 0.5}])
        
        # Must have non-authority clauses
        assert "non_guarantees" in output
        assert "authority_neutrality" in output
        assert "does not recommend actions" in output["non_guarantees"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
