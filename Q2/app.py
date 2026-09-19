import time
import joblib
import redis
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


model = joblib.load("model.joblib")


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

    
    label = model.predict([req.text])[0]


    r.set(req.text, label, ex=CACHE_TTL_SECONDS)

    elapsed_ms = (time.time() - start) * 1000
    return {"label": label, "cached": False, "elapsed_ms": elapsed_ms}
