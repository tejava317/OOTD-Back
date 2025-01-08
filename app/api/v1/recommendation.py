from fastapi import APIRouter, HTTPException
import json
from app.core.config import settings
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse
)
from app.services.gemini import Gemini

# Initialize the router handling requests
router = APIRouter()

GEMINI_API_KEY = settings.GEMINI_API_KEY
gemini = Gemini(GEMINI_API_KEY)

@router.post("/generate-recommendation", response_model=RecommendationResponse)
async def generate_recommendation(request: RecommendationRequest):
    try:
        prompt = (
            "Recommend an outfit based on the following weather information.\n"
            f"Actual temperature: {request.actual_temp}°C\n"
            f"Apparent temperature: {request.apparent_temp}°C\n"
            f"Precipitation: {request.precipitation}mm\n"
            f"Humidity: {request.humidity}%\n"
            f"Wind Speed: {request.wind_speed}m/s\n"
            f"Condition: {request.condition}\n"
            f"Temperature at 6 am: {request.temp_6am}°C\n"
            f"Temperature at 12 pm: {request.temp_12pm}°C\n"
            f"Temperature at 6 pm: {request.temp_6pm}°C\n"
            f"Temperature at 12 am: {request.temp_12am}°C\n"
            "Recommend warmer clothing if its raining or very windy.\n"
            "Recommend a thicker outer garment and slightly lighter tops if the daily temperature range is large.\n"
            "Pick an appropriate option from the following choices to complete outfit and complete json format.\n"
            "겉옷: [두꺼운 패딩, 울 코트, 경량 패딩, 가벼운 재킷, 겉옷 없음]\n"
            "상의: [두꺼운 니트, 긴팔 티셔츠, 반팔 티셔츠]\n"
            "하의: [기모 바지, 긴 바지, 반바지]\n"
            "신발: [부츠, 운동화, 샌들/슬리퍼]\n"
            "Answer in Korean while adhering to the following json format.\n"
            "겉옷: \n"
            "상의: \n"
            "하의: \n"
            "신발: \n"
        )
        response = gemini.get_response(prompt)
        
        response = response.replace('```json', '').replace('```', '').strip()
        parsed_response = json.loads(response)

        return RecommendationResponse(
            message="Outfit recommendation successfully returned.",
            outer=parsed_response["겉옷"],
            top=parsed_response["상의"],
            bottom=parsed_response["하의"],
            shoes=parsed_response["신발"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
