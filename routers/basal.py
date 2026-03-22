from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import get_current_user
from core.dependencies import get_basal_service
from schemas.basal import BasalCreate, BasalResponse
from services.basal_service import BasalService

basal_router = APIRouter()


@basal_router.post(
    "",
    response_model=BasalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log a basal insulin dose",
)
def create_basal(
    payload: BasalCreate,
    current_user=Depends(get_current_user),
    service: BasalService = Depends(get_basal_service),
):
    """
    Save a basal insulin event to the database.

    - **units**: Required. Dose in units (safety cap: 60u)
    - **insulin**: `Glargine` | `Degludec` | `Tresiba`
    - **time**: `Night` | `Morning`
    """
    try:
        return service.create_basal(payload, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
