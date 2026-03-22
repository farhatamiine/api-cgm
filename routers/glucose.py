from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Dict, Any
from utils.glucose import calculate_bmi
from schemas.glucose import GlucoseFullReport
from services.glucose_service import GlucoseService
from core.auth import get_current_user
from core.dependencies import get_glucose_service
from db.models.user import User

glucose_router = APIRouter()


@glucose_router.get("/report", response_model=GlucoseFullReport)
def get_report(
    days: str = Query(default="4", description="Number of past days to look back"),
    current_user: User = Depends(get_current_user),
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
def analyse(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Analyzes user-specific data like BMI and basal units.
    """
    return {
        "user": current_user.full_name,
        "bmi": calculate_bmi(current_user),
        "basal_units": current_user.basal_unit,
    }
