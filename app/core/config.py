from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    
    S3_BUCKET_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()
