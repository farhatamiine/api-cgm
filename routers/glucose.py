from fastapi import APIRouter, Depends, Query, HTTPException
from models.user import User
from typing import Dict,Any
from utils.glucose import caluclate_bmi
from schemas.glucose import GlucoseFullReport
from services.glucose_service import GlucoseService
from core.dependencies import get_glucose_service

glucose_router=APIRouter()





@glucose_router.get('/report',response_model=GlucoseFullReport)
def get_report(
    count: int = Query(default=1152, ge=1, le=10000, description="Number of CGM readings"),
    days: str = Query(default="4", description="Number of past days"),
    service: GlucoseService = Depends(get_glucose_service)):
    try:
        return service.get_full_report(count=count, days=days)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@glucose_router.post('/analyse')
def analyse(user:User) -> Dict[str,Any]:
    if not user:
        return {"error":"User not provided"}
    return { "user": user.full_name,"bmi": caluclate_bmi(user),"basal_units": user.basal_unit}