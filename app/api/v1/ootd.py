# /app/api/v1/ootd.py
# Process all requests starting with '/api/v1/ootd'

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.ootd import (
    PresignedUrlRequest,
    PresignedUrlResponse,
    SaveOOTDRequest,
    SaveOOTDResponse,
    UpdateSatisfactionRequest,
    GetOOTDResponse,
    OOTDInfo,
    GetSimilarOOTDResponse
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
        
        weather_info = db.query(WeatherInfo).filter(
            WeatherInfo.weather_id == weather.weather_id
        ).first()
        if not weather_info:
            weather_info = WeatherInfo(
                weather_id=weather.weather_id,
                actual_temp=request.actual_temp,
                apparent_temp=request.apparent_temp,
                precipitation=request.precipitation,
                humidity=request.precipitation,
                wind_speed=request.wind_speed,
                condition=request.condition,
                temp_6am=request.temp_6am,
                temp_12pm=request.temp_12pm,
                temp_6pm=request.temp_6pm,
                temp_12am=request.temp_12am
            )
            db.add(weather_info)
            db.commit()
            db.refresh(weather_info)

        ootd = db.query(OOTD).filter(
            OOTD.kakao_id == request.kakao_id,
            OOTD.weather_id == weather.weather_id
        ).first()
        if ootd:
            ootd.photo_url = str(request.photo_url)
        else:
            ootd = OOTD(
                kakao_id=request.kakao_id,
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
            OOTD.kakao_id == request.kakao_id,
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

@router.get("/get-ootd-info", response_model=GetOOTDResponse)
def get_ootd_photo(
    kakao_id: int = Query(...),
    date: str = Query(...),
    location: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        ootd = db.query(OOTD).join(Weather).filter(
            OOTD.kakao_id == kakao_id,
            Weather.date == date,
            Weather.location == location
        ).first()
        if not ootd:
            raise HTTPException(status_code=404, detail="OOTD record not found")
        
        return GetOOTDResponse(
            message="OOTD photo successfully returned.",
            photo_url=ootd.photo_url,
            satisfaction_score=ootd.satisfaction_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get OOTD information: {str(e)}")

@router.get("/get-similar-ootd", response_model=GetSimilarOOTDResponse)
def get_similar_ootd(
    kakao_id: int = Query(...),
    apparent_temp: float = Query(...),
    db: Session = Depends(get_db)
):
    try:
        lower_bound = apparent_temp - 1.0
        upper_bound = apparent_temp + 1.0

        similar_ootds = (
            db.query(OOTD.photo_url, OOTD.satisfaction_score)
            .join(Weather, OOTD.weather_id == Weather.weather_id)
            .join(WeatherInfo, Weather.weather_id == WeatherInfo.weather_id)
            .filter(OOTD.kakao_id == kakao_id,
                    WeatherInfo.apparent_temp >= lower_bound,
                    WeatherInfo.apparent_temp <= upper_bound)
            .all()
        )

        ootd_list: List[OOTDInfo] = [
            OOTDInfo(photo_url=row.photo_url, satisfaction_score=row.satisfaction_score)
            for row in similar_ootds
        ]
        
        return GetSimilarOOTDResponse(
            message="Similar OOTDs successfully returned.",
            ootd_list=ootd_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get similar OOTD information: {str(e)}")
