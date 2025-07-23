import pandas as pd
from fastapi import APIRouter, HTTPException
from models.schemas import FlightFeatures
from services.prediction_service import model, model_loaded, preprocessor

router = APIRouter()


@router.post("/predict")
def predict_delay(features: FlightFeatures):
    if not model_loaded:
        raise HTTPException(status_code=500, detail="Model not loaded")

    data = pd.DataFrame([features.dict()])
    X = preprocessor.transform(data)
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0][1]

    return {"prediction": int(prediction), "delay_probability": round(proba, 4)}
