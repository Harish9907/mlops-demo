from fastapi import FastAPI, Response
from pydantic import BaseModel
import joblib
import numpy as np
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()
model = joblib.load("models/model.pkl")

PREDICTIONS = Counter("predictions_total", "Total predictions", ["class"])

class Input(BaseModel):
    features: list

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(inp: Input):
    X = np.array([inp.features])
    pred = model.predict(X)[0]
    PREDICTIONS.labels(class_=str(pred)).inc()
    return {"prediction": int(pred)}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

