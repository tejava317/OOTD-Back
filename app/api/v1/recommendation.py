from fastapi import APIRouter, HTTPException
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
        prompt = "Hello"
        response = gemini.get_response(prompt)
        return RecommendationResponse(message=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
