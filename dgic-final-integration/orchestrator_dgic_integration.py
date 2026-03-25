"""
Orchestrator → DGIC Integration Layer
Owner: Pritesh Patra
Consumer: Aakanksha Parab (AI Being Orchestrator)

This module provides the integration interface for the Orchestrator to call DGIC.
"""

import requests
import uuid
import time
from typing import List, Dict, Optional


class DGICIntegrationError(Exception):
    """Raised when DGIC integration fails"""
    pass


class OrchestratorDGICClient:
    """
    Client for Orchestrator to communicate with DGIC.
    
    Usage:
        client = OrchestratorDGICClient(dgic_url="http://localhost:8000")
        response = client.evaluate_decision(signals=[...])
    """
    
    def __init__(self, dgic_url: str = "http://localhost:8000"):
        self.dgic_url = dgic_url.rstrip("/")
        self.endpoint = f"{self.dgic_url}/dgic/evaluate"
    
    def evaluate_decision(
        self,
        signals: List[Dict],
        execution_id: Optional[str] = None
    ) -> Dict:
        """
        Send signals to DGIC and receive decision.
        
        Args:
            signals: List of signal dictionaries with keys:
                - id: str (unique identifier)
                - type: str (THREAT | SAFE | UNKNOWN)
                - priority: float (0.0-1.0)
                - timestamp: int (Unix epoch ms)
                - source: str (agent identifier)
                - metadata: dict (optional)
            execution_id: Optional UUID v4 string. If not provided, one is generated.
        
        Returns:
            Dict containing:
                - execution_id: str
                - timestamp: int
                - decision: str (ESCALATE | PROCEED | HOLD | REQUEST_MORE_DATA | ERROR)
                - confidence: float
                - epistemic_state: str
                - collapse_trigger: str
                - execution_hash: str
                - processing_time_ms: int
        
        Raises:
            DGICIntegrationError: If request fails or validation errors occur
        """
        
        # Generate execution_id if not provided
        if execution_id is None:
            execution_id = str(uuid.uuid4())
        
        # Validate execution_id format
        try:
            uuid.UUID(execution_id, version=4)
        except ValueError:
            raise DGICIntegrationError(f"Invalid execution_id format: {execution_id}")
        
        # Validate signals
        if not signals:
            raise DGICIntegrationError("signals list cannot be empty")
        
        if len(signals) > 100:
            raise DGICIntegrationError("signals list cannot exceed 100 elements")
        
        # Build request payload
        request_payload = {
            "execution_id": execution_id,
            "timestamp": int(time.time() * 1000),
            "signals": signals
        }
        
        # Make request to DGIC
        try:
            response = requests.post(
                self.endpoint,
                json=request_payload,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.ConnectionError:
            raise DGICIntegrationError("DGIC service unreachable")
        
        except requests.exceptions.Timeout:
            raise DGICIntegrationError("DGIC request timed out")
        
        except requests.exceptions.HTTPError as e:
            error_detail = e.response.json() if e.response.content else str(e)
            raise DGICIntegrationError(f"DGIC returned error: {error_detail}")
        
        except Exception as e:
            raise DGICIntegrationError(f"Unexpected error: {str(e)}")
    
    def create_signal(
        self,
        signal_id: str,
        signal_type: str,
        priority: float,
        source: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Helper method to create a properly formatted signal.
        
        Args:
            signal_id: Unique identifier for the signal
            signal_type: THREAT | SAFE | UNKNOWN
            priority: 0.0-1.0
            source: Agent identifier
            metadata: Optional metadata dictionary
        
        Returns:
            Dict representing a valid signal
        """
        
        if signal_type not in ["THREAT", "SAFE", "UNKNOWN"]:
            raise ValueError(f"Invalid signal_type: {signal_type}")
        
        if not (0.0 <= priority <= 1.0):
            raise ValueError(f"priority must be between 0.0 and 1.0, got {priority}")
        
        signal = {
            "id": signal_id,
            "type": signal_type,
            "priority": priority,
            "timestamp": int(time.time() * 1000),
            "source": source
        }
        
        if metadata:
            signal["metadata"] = metadata
        
        return signal


# Convenience function for quick integration
def call_dgic(signals: List[Dict], dgic_url: str = "http://localhost:8000") -> Dict:
    """
    Quick function to call DGIC with signals.
    
    Args:
        signals: List of signal dictionaries
        dgic_url: DGIC service URL
    
    Returns:
        DGIC response dictionary
    """
    client = OrchestratorDGICClient(dgic_url=dgic_url)
    return client.evaluate_decision(signals=signals)
