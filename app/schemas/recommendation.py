from pydantic import BaseModel

class RecommendationRequest(BaseModel):
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

class RecommendationResponse(BaseModel):
    message: str
