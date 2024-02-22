from typing import Annotated

from common.schema import Intensity, PositiveRoundedFloat
from pydantic import BaseModel, Field


class DroughtIntensity(Intensity):
    duration_months: PositiveRoundedFloat
    severity: PositiveRoundedFloat


class ReturnPeriod(BaseModel):
    intensity: DroughtIntensity
    vulnerability: str


class DroughtRiskAssessment(BaseModel):
    return_period_20y: ReturnPeriod
    return_period_100y: ReturnPeriod
    return_period_200y: ReturnPeriod


class OutputSchema(BaseModel):
    address: str | None
    lat: Annotated[float, Field(ge=-90, le=90)]
    lon: Annotated[float, Field(ge=-180, le=180)]
    drought_risk_assessment: DroughtRiskAssessment
