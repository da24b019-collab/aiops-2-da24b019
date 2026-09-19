import time
import joblib
import redis
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Load the trained pipeline once at startup
model = joblib.load("model.joblib")

# Connect to Redis. "cache" is the hostname we'll use inside Docker Compose —
# Compose lets containers reach each other by service name.
# decode_responses=True means we get plain strings back, not bytes.
r = redis.Redis(host="cache", port=6379, decode_responses=True)

CACHE_TTL_SECONDS = 60  # how long a cached prediction stays valid

class PredictRequest(BaseModel):
    text: str

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    start = time.time()

    # Use the exact input text as the Redis cache key
    cached_label = r.get(req.text)

    if cached_label is not None:
        # Cache HIT — skip the model entirely
        elapsed_ms = (time.time() - start) * 1000
        return {"label": cached_label, "cached": True, "elapsed_ms": elapsed_ms}

    # Cache MISS — compute the prediction
    label = model.predict([req.text])[0]

    # Store it in Redis with a TTL so old predictions eventually expire
    r.set(req.text, label, ex=CACHE_TTL_SECONDS)

    elapsed_ms = (time.time() - start) * 1000
    return {"label": label, "cached": False, "elapsed_ms": elapsed_ms}
