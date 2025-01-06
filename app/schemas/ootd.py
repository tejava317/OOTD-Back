from pydantic import BaseModel, HttpUrl, Field
from datetime import date

class PresignedUrlRequest(BaseModel):
    file_name: str
    file_type: str

class PresignedUrlResponse(BaseModel):
    presigned_url: HttpUrl
    file_url: HttpUrl

class SaveOOTDRequest(BaseModel):
    user_id: int
    date: date
    location: str
    actual_temp: float
    apparent_temp: float
    precipitation: float
    humidity: int
    wind_speed: float
    temp_6am: float
    temp_12pm: float
    temp_6pm: float
    temp_12am: float
    photo_url: HttpUrl

class SaveOOTDResponse(BaseModel):
    message: str
    ootd_id: int

class UpdateSatisfactionRequest(BaseModel):
    user_id: int
    date: date
    location: str
    satisfaction_score: int = Field(..., ge=1, le=5)
