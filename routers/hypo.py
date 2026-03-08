from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.dependencies import get_hypo_service
from schemas.hypo import HypoCreate, HypoResponse
from services.hypo_service import HypoService

hypo_router = APIRouter()


@hypo_router.post(
    "",
    response_model=HypoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log a hypoglycaemic event",
)
def log_hypo(
    payload: HypoCreate,
    service: HypoService = Depends(get_hypo_service),
):
    """
    Save a hypo event to the database.

    - **lowest_value**: Required. Must be ≤ 70 mg/dL
    - **started_at**: Required. When the hypo started
    - **duration_min**: Auto-calculated if ended_at is provided
    """
    try:
        return service.create_hypo(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@hypo_router.get(
    "",
    response_model=List[HypoResponse],
    summary="List hypo events",
)
def list_hypos(
    limit: int = Query(default=20, ge=1, le=100, description="Max results to return"),
    service: HypoService = Depends(get_hypo_service),
):
    """Returns hypo events ordered by most recent first."""
    try:
        return service.list_hypos(limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
