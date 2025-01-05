from pydantic import BaseModel, HttpUrl

class PresignedUrlRequest(BaseModel):
    file_name: str
    file_type: str

class PresignedUrlResponse(BaseModel):
    presigned_url: HttpUrl
    file_url: HttpUrl

class SaveOOTDRequest(BaseModel):
    user_id: int
    weather_id: int
    photo_url: HttpUrl
