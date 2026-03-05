from pydantic import BaseModel, Field




class GlucoseQueryParams(BaseModel):
    """Query parameters for fetching glucose data."""
    count: int = Field(default=1152, ge=1, le=10000, description="Number of CGM readings to fetch")
    days: str = Field(default="4", description="Number of past days (e.g. '4', '7', '30')")


class GlucoseStats(BaseModel):
    average: float = Field(..., description="Mean glucose in mg/dL")
    gmi: float = Field(..., description="Glucose Management Indicator (estimated A1c %)")
    
    
class GlucoseMetadata(BaseModel):
    period_days: int
    total_readings: int

    
class GlucoseRanges(BaseModel):
    tir: float = Field(..., description="Time In Range 70–180 mg/dL (%)")
    high: float = Field(..., description="Time Above Range >180 mg/dL (%)")
    low: float = Field(..., description="Time Below Range <70 mg/dL (%)")


class GlucoStatsResponse(BaseModel):
    metadata: GlucoseMetadata
    stats: GlucoseStats
    ranges: GlucoseRanges