from fastapi import APIRouter, Depends, Query, HTTPException
from schemas.bolus import BolusTimingResponse
from services.glucose_service import GlucoseService
from core.dependencies import get_glucose_service

bolus_router=APIRouter()





@bolus_router.get('/timing',response_model=BolusTimingResponse)
def get_bolus(
    meal_type: str = Query(default="medium_gi", description="Type of meal (low_gi, medium_gi, high_gi)"),
    service: GlucoseService = Depends(get_glucose_service)):
    """
    Calculates the optimal timing for an insulin bolus based on current glucose level and meal GI.
    """
    try:
        return service.get_bolus_timing(meal_type=meal_type)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))