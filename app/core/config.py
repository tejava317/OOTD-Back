from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    DATABASE_URL: str

    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    S3_BUCKET_NAME: str

    KAKAO_AUTH_URL: ClassVar[str] = "https://kauth.kakao.com"
    KAKAO_API_URL: ClassVar[str]= "https://kapi.kakao.com"

    KAKAO_CLIENT_ID: str
    KAKAO_CLIENT_SECRET: str
    KAKAO_REDIRECT_URI: str

    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
