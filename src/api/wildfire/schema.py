from typing import Annotated

from common.schema import (
    NOT_IMPLEMENTED_PLACEHOLDER,
    Intensity,
    PositiveRoundedFloat,
    Probability,
)
from pydantic import BaseModel, Field, conint


class WildfireIntensity(Intensity):
    fwi: PositiveRoundedFloat


class ReturnPeriod(BaseModel):
    intensity: WildfireIntensity
    vulnerability: Probability


class WildfireRiskAssessment(BaseModel):
    return_period_2y: ReturnPeriod
    return_period_10y: ReturnPeriod
    return_period_30y: ReturnPeriod


class AverageAnnualLoss(BaseModel):
    value: Probability
    national_average: Probability
    regional_average: type(NOT_IMPLEMENTED_PLACEHOLDER)


class OutputSchema(BaseModel):
    address: str | None
    lat: Annotated[float, Field(ge=-90, le=90)]
    lon: Annotated[float, Field(ge=-180, le=180)]
    land_use: str
    wildfire_risk_assessment: WildfireRiskAssessment
    risk_index: conint(ge=0, le=5)
    average_annual_loss: AverageAnnualLoss
    hazard_index: type(NOT_IMPLEMENTED_PLACEHOLDER)
