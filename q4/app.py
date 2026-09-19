import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

model = joblib.load("model.joblib")

VERSION = os.environ.get("APP_VERSION", "v1")

class PredictRequest(BaseModel):
    text: str

@app.get("/healthz")
def healthz():
    return {"status": "ok", "version": VERSION}

@app.post("/predict")
def predict(req: PredictRequest):
    label = model.predict([req.text])[0]
    return {"label": label}
