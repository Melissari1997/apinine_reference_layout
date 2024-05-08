from typing import Annotated

from common.schema import (
    NOT_IMPLEMENTED_PLACEHOLDER,
    Intensity,
    PositiveRoundedFloat,
    Probability,
)
from pydantic import BaseModel, Field

PositiveInt = Annotated[int, Field(ge=0)]


class FloodIntensity(Intensity):
    water_height: PositiveRoundedFloat


class ReturnPeriod(BaseModel):
    intensity: FloodIntensity
    vulnerability: Probability


class FloodRiskAssessment(BaseModel):
    return_period_20y: ReturnPeriod
    return_period_100y: ReturnPeriod
    return_period_200y: ReturnPeriod


class AverageAnnualLoss(BaseModel):
    value: PositiveRoundedFloat
    national_average: PositiveRoundedFloat
    regional_average: type(NOT_IMPLEMENTED_PLACEHOLDER)


class OutputSchema(BaseModel):
    address: str | None
    lat: Annotated[float, Field(ge=-90, le=90)]
    lon: Annotated[float, Field(ge=-180, le=180)]
    land_use: str
    flood_risk_assessment: FloodRiskAssessment
    risk_index: PositiveInt
    average_annual_loss: AverageAnnualLoss
    hazard_index: type(NOT_IMPLEMENTED_PLACEHOLDER)
