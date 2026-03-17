import requests


class InsightBridgeAdapter:
    """
    Simulates InsightBridge sending anomaly signals to DGIC
    """

    def __init__(self, dgic_url="http://127.0.0.1:8000/dgic/evaluate"):
        self.dgic_url = dgic_url

    def send_signal(self, signals):
        request_data = {
            "signals": signals,
            "context": {"source": "InsightBridge"},
            "source_system": "INSIGHTBRIDGE",
            "prior_state": {},
        }

        try:
            response = requests.post(self.dgic_url, json=request_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "DGIC service unreachable"}
        except requests.exceptions.Timeout:
            return {"error": "DGIC request timed out"}
        except requests.exceptions.HTTPError as e:
            return {"error": str(e)}