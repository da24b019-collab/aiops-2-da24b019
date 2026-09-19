import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

model = joblib.load("model.joblib")

class PredictRequest(BaseModel):
    text: str

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    label = model.predict([req.text])[0]
    return {"label": label}
