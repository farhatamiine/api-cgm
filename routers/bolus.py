from fastapi import APIRouter, Depends, Query, HTTPException
from schemas.bolus import BolusTimingResponse
from services.glucose_service import GlucoseService
from core.dependencies import get_glucose_service

bolus_router=APIRouter()





@bolus_router.get('/timing',response_model=BolusTimingResponse)
def get_bolus(
    meal_type: str = Query(default="medium_gi", description="Number of CGM readings"),
    service: GlucoseService = Depends(get_glucose_service)):
    try:
        return service.get_bolus_timing(meal_type=meal_type)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))