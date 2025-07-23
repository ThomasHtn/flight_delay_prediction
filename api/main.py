import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load model and preprocessor once at startup
try:
    model = joblib.load("ml/models/final_model.pkl")
    preprocessor = joblib.load("ml/models/preprocessor.pkl")
    model_loaded = True
except Exception as e:
    model_loaded = False
    print(f"❌ Model loading failed: {e}")

app = FastAPI(title="Flight Delay Prediction API")


class FlightFeatures(BaseModel):
    month: int
    day_of_week: int
    crs_dep_time: int
    crs_arr_time: int
    crs_elapsed_time: int
    distance: float
    unique_carrier: str
    origin: str
    dest: str
    dep_time_blk: str


@app.get("/health")
def health_check():
    """
    Basic health check endpoint to verify model and preprocessor availability.
    """
    if model_loaded:
        return {"status": "ok", "message": "Model and preprocessor loaded."}
    else:
        raise HTTPException(status_code=500, detail="Model not loaded")


@app.post("/predict")
def predict_delay(features: FlightFeatures):
    if not model_loaded:
        raise HTTPException(status_code=500, detail="Model not loaded")

    data = pd.DataFrame([features.dict()])
    X = preprocessor.transform(data)
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0][1]

    return {"prediction": int(prediction), "delay_probability": round(proba, 4)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
