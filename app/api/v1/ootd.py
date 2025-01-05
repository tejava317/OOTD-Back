from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.ootd import PresignedUrlRequest, PresignedUrlResponse, SaveOOTDRequest
from app.models.ootd import OOTD
from app.db.session import get_db
from app.services.s3_service import S3Service
from app.core.config import settings

router = APIRouter()

s3_service = S3Service(
    aws_access_key=settings.AWS_ACCESS_KEY,
    aws_secret_key=settings.AWS_SECRET_KEY,
    aws_region=settings.AWS_REGION,
    bucket_name=settings.S3_BUCKET_NAME
)

@router.post("/generate-presigned-url", response_model=PresignedUrlResponse)
def generate_presigned_url(request: PresignedUrlRequest):
    try:
        response = s3_service.generate_presigned_url(request.file_name, request.file_type)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-ootd")
def save_ootd(request: SaveOOTDRequest, db: Session = Depends(get_db)):
    try:
        new_ootd = OOTD(
            user_id=request.user_id,
            weather_id = request.weather_id,
            photo_url=str(request.photo_url)
        )
        db.add(new_ootd)
        db.commit()
        return {"message": "OOTD saved successfully", "ootd_id": new_ootd.ootd_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save OOTD: {str(e)}")
