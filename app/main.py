from fastapi import FastAPI
from app.api.v1 import weather, auth

app = FastAPI(
    title="OOTD Backend API",
    description="API for weather-based outfit recommendation",
    version="1.0.0"
)

app.include_router(weather.router, prefix="/api/v1/weather", tags=["Weather"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to OOTD Backend API"}
