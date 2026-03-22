from fastapi import APIRouter, Depends, Query, HTTPException
from models.user import User
from typing import Dict, Any
from utils.glucose import calculate_bmi
from schemas.glucose import GlucoseFullReport
from services.glucose_service import GlucoseService
from core.dependencies import get_glucose_service

glucose_router = APIRouter()


@glucose_router.get("/report", response_model=GlucoseFullReport)
def get_report(
    days: str = Query(default="4", description="Number of past days to look back"),
    service: GlucoseService = Depends(get_glucose_service),
):
    """
    Generates a full report including stats, variability, patterns, and dawn phenomenon analysis.
    """
    try:
        return service.get_full_report(days=days)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@glucose_router.post("/analyse")
def analyse(user: User) -> Dict[str, Any]:
    """
    Analyzes user-specific data like BMI and basal units.
    """
    if not user:
        return {"error": "User not provided"}
    return {
        "user": user.full_name,
        "bmi": calculate_bmi(user),
        "basal_units": user.basal_unit,
    }
