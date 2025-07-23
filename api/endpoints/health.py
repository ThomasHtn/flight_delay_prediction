from fastapi import APIRouter, HTTPException
from services.prediction_service import model_loaded

router = APIRouter()


@router.get("/health")
def health_check():
    if model_loaded:
        return {"status": "ok", "message": "Model and preprocessor loaded."}
    raise HTTPException(status_code=500, detail="Model not loaded")
