from pydantic import BaseModel, Field
from typing import Any



class BolusTimingResponse(BaseModel):
    """Response model for optimal insulin bolus timing."""
    inject_minutes_before: int = Field(..., description="Recommended lead time in minutes before eating")
    message: str = Field(..., description="Actionable advice for the user")
    warning: Any = Field(None, description="Critical warning if glucose is too high for safe bolusing")