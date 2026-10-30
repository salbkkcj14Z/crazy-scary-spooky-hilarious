from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import hmac
import hashlib
import time

app = FastAPI(title="Cognitive Telemetry Engine", version="1.0.0")

SECRET_KEY = b"cognitive_emergence_shared_secret"

class TelemetryPayload(BaseModel):
    node_id: str
    intent_vector: str
    confidence_score: float
    timestamp: float

@app.post("/telemetry/ingest")
async def ingest_telemetry(payload: TelemetryPayload, x_signature: str = Header(None)):
    start_time = time.perf_counter_ns()
    
    # Zero-trust signature validation
    payload_bytes = payload.model_dump_json().encode('utf-8')
    expected_sig = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest()
    
    if not x_signature or not hmac.compare_digest(expected_sig, x_signature):
        raise HTTPException(status_code=403, detail="Tamper detection triggered: Invalid signature.")
    
    latency_us = (time.perf_counter_ns() - start_time) / 1000.0
    
    return {
        "status": "synchronized",
        "node": payload.node_id,
        "latency_us": latency_us,
        "state": "uncollapsed"
    }

