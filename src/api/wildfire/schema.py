from typing import Annotated

from common.schema import Intensity, PositiveRoundedFloat
from pydantic import BaseModel, Field


class WildfireIntensity(Intensity):
    fwi: PositiveRoundedFloat


class ReturnPeriod(BaseModel):
    intensity: WildfireIntensity
    vulnerability: str


class WildfireRiskAssessment(BaseModel):
    return_period_2y: ReturnPeriod
    return_period_10y: ReturnPeriod
    return_period_30y: ReturnPeriod


class OutputSchema(BaseModel):
    address: str | None
    lat: Annotated[float, Field(ge=-90, le=90)]
    lon: Annotated[float, Field(ge=-180, le=180)]
    wildfire_risk_assessment: WildfireRiskAssessment
