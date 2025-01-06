# /app/api/v1/ootd.py
# Process all requests starting with '/api/v1/ootd'

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.ootd import (
    PresignedUrlRequest,
    PresignedUrlResponse,
    SaveOOTDRequest,
    SaveOOTDResponse,
    UpdateSatisfactionRequest
)
from app.models.weather import Weather
from app.models.weather_info import WeatherInfo
from app.models.ootd import OOTD
from app.db.session import get_db
from app.services.s3_service import S3Service
from app.core.config import settings

# Initialize the router handling requests
router = APIRouter()

AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_KEY = settings.AWS_SECRET_KEY
AWS_REGION = settings.AWS_REGION
BUCKET_NAME = settings.S3_BUCKET_NAME

s3_service = S3Service(
    aws_access_key=AWS_ACCESS_KEY,
    aws_secret_key=AWS_SECRET_KEY,
    aws_region=AWS_REGION,
    bucket_name=BUCKET_NAME
)

@router.post("/generate-presigned-url", response_model=PresignedUrlResponse)
def generate_presigned_url(request: PresignedUrlRequest):
    try:
        response = s3_service.generate_presigned_url(request.file_name, request.file_type)
        return {
            "presigned_url": response["presignedUrl"],
            "file_url": response["fileUrl"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-ootd", response_model=SaveOOTDResponse)
def save_ootd(request: SaveOOTDRequest, db: Session = Depends(get_db)):
    try:
        weather = db.query(Weather).filter(
            Weather.date == request.date,
            Weather.location == request.location
        ).first()
        if not weather:
            weather = Weather(date=request.date, location=request.location)
            db.add(weather)
            db.commit()
            db.refresh(weather)

        ootd = db.query(OOTD).filter(
            OOTD.user_id == request.user_id,
            OOTD.weather_id == weather.weather_id
        ).first()
        if ootd:
            ootd.photo_url = str(request.photo_url)
        else:
            ootd = OOTD(
                user_id=request.user_id,
                weather_id=weather.weather_id,
                photo_url=str(request.photo_url),
                satisfaction_score=None
            )
            db.add(ootd)
        db.commit()
        db.refresh(ootd)

        return SaveOOTDResponse(
            message="OOTD successfully saved.",
            ootd_id=ootd.ootd_id
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save OOTD: {str(e)}")

@router.put("/update-satisfaction")
def update_satisfaction(request: UpdateSatisfactionRequest, db: Session = Depends(get_db)):
    try:
        ootd = db.query(OOTD).join(Weather).filter(
            OOTD.user_id == request.user_id,
            Weather.date == request.date,
            Weather.location == request.location
        ).first()

        if not ootd:
            raise HTTPException(status_code=404, detail="OOTD record not found")

        # Update satisfaction score
        ootd.satisfaction_score = request.satisfaction_score
        db.commit()
        db.refresh(ootd)

        return {"message": "Satisfaction score updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update satisfaction score: {str(e)}")
