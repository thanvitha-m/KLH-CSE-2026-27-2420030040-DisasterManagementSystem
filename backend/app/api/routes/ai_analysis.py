from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.services.groq_service import analyze_disaster

router = APIRouter()


class AIAnalysisRequest(BaseModel):
    disaster_details: str = Field(min_length=10, max_length=3000)
    route_details: str = Field(default="", max_length=3000)


@router.post("/analyze")
def analyze_with_ai(request: AIAnalysisRequest):
    try:
        analysis = analyze_disaster(
            disaster_details=request.disaster_details,
            route_details=request.route_details,
        )

        return {
            "status": "success",
            "model": "openai/gpt-oss-20b",
            "analysis": analysis,
            "disclaimer": "Academic simulation only. Not verified emergency guidance.",
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="AI analysis is temporarily unavailable. Please try again.",
        )
