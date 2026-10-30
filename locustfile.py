import hmac
import hashlib
import json
import time
from locust import HttpUser, task, between

SECRET_KEY = b"cognitive_emergence_shared_secret"

class CognitiveTelemetryUser(HttpUser):
    wait_time = between(0.001, 0.01)  # High-frequency intent streaming

    @task
    def send_telemetry(self):
        payload = {
            "node_id": f"node-{id(self)}",
            "intent_vector": "vector-state-space-bulk-verify",
            "confidence_score": 0.999,
            "timestamp": time.time()
        }
        
        # Use compact separators to match deterministic JSON encoding
        payload_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')
        signature = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest()
        
        headers = {
            "Content-Type": "application/json",
            "x-signature": signature
        }
        
        self.client.post("/telemetry/ingest", json=payload, headers=headers)
