import hmac
import hashlib
import json
import time
import requests

URL = "http://localhost:8000/telemetry/ingest"
SECRET_KEY = b"cognitive_emergence_shared_secret"

def test_telemetry_ingest():
    payload = {
        "node_id": "node-alpha-01",
        "intent_vector": "vector-state-space-zero",
        "confidence_score": 0.998,
        "timestamp": time.time()
    }

    payload_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    signature = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "x-signature": signature
    }

    start = time.perf_counter()
    response = requests.post(URL, json=payload, headers=headers)
    duration = (time.perf_counter() - start) * 1000.0

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Roundtrip Latency: {duration:.3f} ms")

if __name__ == "__main__":
    test_telemetry_ingest()
