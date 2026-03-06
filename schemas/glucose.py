from pydantic import BaseModel, Field




class GlucoseQueryParams(BaseModel):
    """Query parameters for fetching glucose data."""
    count: int = Field(default=1152, ge=1, le=10000, description="Number of CGM readings to fetch")
    days: str = Field(default="4", description="Number of past days (e.g. '4', '7', '30')")


class GlucoseStats(BaseModel):
    average: float = Field(..., description="Mean glucose in mg/dL")
    gmi: float = Field(..., description="Glucose Management Indicator (estimated A1c %)")
    
    
class GlucoseMetadata(BaseModel):
    period_days: str
    total_readings: int

    
class GlucoseRanges(BaseModel):
    tir: float = Field(..., description="Time In Range 70–180 mg/dL (%)")
    tar: float = Field(..., description="Time Above Range >180 mg/dL (%)")
    tbr: float = Field(..., description="Time Below Range <70 mg/dL (%)")


class GlucoStatsResponse(BaseModel):
    metadata: GlucoseMetadata
    stats: GlucoseStats
    ranges: GlucoseRanges
    
    
class GlucoVariabilityResponse(BaseModel):
    std_dev:float = Field(...,description='Standard Deviation:How far your glucose readings scatter around your average.')
    cv:float = Field(...,description='Coefficient of Variation:The most important variability number.')
    highest:float = Field(...,description='Highest reading in the period → your worst spike')
    lowest:float = Field(...,description='Lowest reading in the period  → your worst hypo')
    flag:str = Field(...,description='Glucose variability')
    

class GlucoseFullReport(BaseModel):
    stats:GlucoStatsResponse
    variability:GlucoVariabilityResponse
    patterns:GlucosePatternResponse
    
class GlucosePattern(BaseModel):
    avg:int
    reading:int
    time:str
    

class GlucosePatternResponse(BaseModel):
    morning:GlucosePattern
    afternoon:GlucosePattern
    evening:GlucosePattern
    night:GlucosePattern
    worst_period:str