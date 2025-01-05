# /app/main.py
# Main application of FastAPI

from fastapi import FastAPI, Depends
from app.api.v1 import auth, ootd
from app.db.session import get_db
from sqlalchemy.orm import Session

# Initialize FastAPI application
app = FastAPI(
    title="OOTD Backend API",
    description="API for weather-based outfit recommendation",
    version="1.0.0"
)

# Register the router (Process requests using handler function)
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(ootd.router, prefix="/api/v1/ootd", tags=["OOTD"])

# Root endpoint (Return welcome message)
@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Welcome to OOTD Backend API"}
