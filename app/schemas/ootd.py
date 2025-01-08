from pydantic import BaseModel, HttpUrl
from typing import List

class PresignedUrlRequest(BaseModel):
    file_name: str
    file_type: str

class PresignedUrlResponse(BaseModel):
    presigned_url: HttpUrl
    file_url: HttpUrl

class SaveOOTDRequest(BaseModel):
    kakao_id: int
    date: str
    location: str
    actual_temp: float
    apparent_temp: float
    precipitation: float
    humidity: int
    wind_speed: float
    condition: str
    temp_6am: float
    temp_12pm: float
    temp_6pm: float
    temp_12am: float
    photo_url: HttpUrl

class SaveOOTDResponse(BaseModel):
    message: str
    ootd_id: int

class UpdateSatisfactionRequest(BaseModel):
    kakao_id: int
    date: str
    location: str
    satisfaction_score: int

class GetOOTDResponse(BaseModel):
    message: str
    photo_url: HttpUrl
    satisfaction_score: int

class OOTDInfo(BaseModel):
    photo_url: HttpUrl
    satisfaction_score: int

class GetSimilarOOTDResponse(BaseModel):
    message: str
    ootd_list: List[OOTDInfo]

class GetAllOOTDResponse(BaseModel):
    message: str
    photo_list: List[HttpUrl]
