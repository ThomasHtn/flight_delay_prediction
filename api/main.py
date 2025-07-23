from fastapi import FastAPI

from endpoints import health, predict

app = FastAPI(title="Flight Delay Prediction API")

# Register routes
app.include_router(health.router)
app.include_router(predict.router)
