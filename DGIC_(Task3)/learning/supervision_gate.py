"""
Supervision Gate

External approval mechanism for learning updates.
Ensures no autonomous learning occurs.
"""

from typing import Optional, Dict, Any
import time


class SupervisionGate:
    """
    Enforces external supervision requirement for all learning.
    
    No learning update proceeds without explicit approval.
    """
    
    def __init__(self):
        self.pending_updates = []
        self.approved_updates = []
        self.rejected_updates = []
    
    def request_approval(
        self,
        update: Dict[str, Any],
        requester: str
    ) -> str:
        """
        Submit learning update for approval.
        Returns request_id for tracking.
        """
        request_id = f"REQ-{int(time.time())}-{len(self.pending_updates)}"
        
        request = {
            "request_id": request_id,
            "update": update,
            "requester": requester,
            "timestamp": time.time(),
            "status": "pending"
        }
        
        self.pending_updates.append(request)
        return request_id
    
    def approve(
        self,
        request_id: str,
        supervisor_id: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Approve pending learning update.
        Only external supervisor can approve.
        """
        request = self._find_request(request_id)
        if not request:
            return False
        
        if not supervisor_id:
            return False
        
        request["status"] = "approved"
        request["supervisor"] = supervisor_id
        request["approval_notes"] = notes
        request["approval_time"] = time.time()
        
        self.pending_updates.remove(request)
        self.approved_updates.append(request)
        
        return True
    
    def reject(
        self,
        request_id: str,
        supervisor_id: str,
        reason: str
    ) -> bool:
        """
        Reject pending learning update.
        """
        request = self._find_request(request_id)
        if not request:
            return False
        
        request["status"] = "rejected"
        request["supervisor"] = supervisor_id
        request["rejection_reason"] = reason
        request["rejection_time"] = time.time()
        
        self.pending_updates.remove(request)
        self.rejected_updates.append(request)
        
        return True
    
    def get_approved_update(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve approved update for application."""
        for update in self.approved_updates:
            if update["request_id"] == request_id:
                return update
        return None
    
    def _find_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Find pending request by ID."""
        for request in self.pending_updates:
            if request["request_id"] == request_id:
                return request
        return None
    
    def get_pending_count(self) -> int:
        """Return number of pending approval requests."""
        return len(self.pending_updates)
