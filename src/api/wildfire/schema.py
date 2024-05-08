from typing import Annotated

from common.schema import NOT_IMPLEMENTED_PLACEHOLDER, Intensity, PositiveRoundedFloat
from pydantic import BaseModel, Field


class WildfireIntensity(Intensity):
    fwi: PositiveRoundedFloat


class ReturnPeriod(BaseModel):
    intensity: WildfireIntensity
    vulnerability: type(NOT_IMPLEMENTED_PLACEHOLDER)


class WildfireRiskAssessment(BaseModel):
    return_period_2y: ReturnPeriod
    return_period_10y: ReturnPeriod
    return_period_30y: ReturnPeriod


class AverageAnnualLoss(BaseModel):
    value: type(NOT_IMPLEMENTED_PLACEHOLDER)
    national_average: type(NOT_IMPLEMENTED_PLACEHOLDER)
    regional_average: type(NOT_IMPLEMENTED_PLACEHOLDER)


class OutputSchema(BaseModel):
    address: str | None
    lat: Annotated[float, Field(ge=-90, le=90)]
    lon: Annotated[float, Field(ge=-180, le=180)]
    wildfire_risk_assessment: WildfireRiskAssessment
    risk_index: type(NOT_IMPLEMENTED_PLACEHOLDER)
    average_annual_loss: AverageAnnualLoss
    hazard_index: type(NOT_IMPLEMENTED_PLACEHOLDER)
