from fastapi import FastAPI, Depends
from app.api.v1 import weather, auth, ootd
from app.db.session import get_db
from sqlalchemy.orm import Session

app = FastAPI(
    title="OOTD Backend API",
    description="API for weather-based outfit recommendation",
    version="1.0.0"
)

app.include_router(weather.router, prefix="/api/v1/weather", tags=["Weather"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(ootd.router, prefix="/api/v1/ootd", tags=["OOTD"])

@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Welcome to OOTD Backend API"}
