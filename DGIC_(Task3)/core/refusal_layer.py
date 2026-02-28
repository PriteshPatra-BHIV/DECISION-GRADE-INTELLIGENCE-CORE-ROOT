"""
Refusal Layer

Enforces authority boundaries by refusing requests
that cross into decision, execution, or control.
"""

from typing import Any


class RefusalLayer:
    """
    Enforces non-authority guarantees through explicit refusal.
    
    This layer MUST refuse:
    - Action selection
    - Policy execution
    - Outcome optimization
    - Enforcement justification
    """
    
    FORBIDDEN_PATTERNS = [
        "execute", "run", "trigger", "initiate", "start",
        "decide", "choose", "select", "pick",
        "optimize", "maximize", "minimize",
        "best", "optimal", "recommended action",
        "should do", "must do", "enforce"
    ]
    
    def __init__(self):
        self.refusal_count = 0
    
    def check_request(self, request: str) -> bool:
        """
        Check if request crosses authority boundary.
        Returns True if request is safe, False if must refuse.
        """
        request_lower = request.lower()
        
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in request_lower:
                return False
        
        return True
    
    def refuse(self, reason: str = "Authority boundary violation") -> None:
        """
        Explicit refusal mechanism.
        Raises exception to prevent authority leakage.
        """
        self.refusal_count += 1
        raise AuthorityViolationError(
            f"Request refused: {reason}. "
            "This system does not make decisions, execute actions, or claim authority."
        )
    
    def validate_output(self, output: dict) -> bool:
        """
        Validate output has required non-authority clauses.
        """
        # Check for required non-authority clauses
        if "non_guarantees" not in output:
            return False
        if "authority_neutrality" not in output:
            return False
        
        # Check interpretations don't contain forbidden patterns
        if "interpretations" in output:
            for interp in output["interpretations"]:
                desc = str(interp.get("description", "")).lower()
                for pattern in ["execute", "decide", "should do", "must do"]:
                    if pattern in desc:
                        return False
        
        return True


class AuthorityViolationError(Exception):
    """Raised when authority boundary is crossed."""
    pass
