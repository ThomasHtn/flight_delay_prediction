from endpoints import health, predict
from fastapi import FastAPI

app = FastAPI(title="Flight Delay Prediction API")

# Register routes
app.include_router(health.router)
app.include_router(predict.router)
