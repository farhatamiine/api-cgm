from pydantic import BaseModel, Field
from typing import Any



class BolusTimingResponse(BaseModel):
    inject_minutes_before: int = Field(..., description="Time In Range 70–180 mg/dL (%)")
    message: str = Field(..., description="Time Above Range >180 mg/dL (%)")
    warning: Any = Field(..., description="Time Below Range <70 mg/dL (%)")