from typing import Annotated

from common.schema import NOT_IMPLEMENTED_PLACEHOLDER, Intensity, PositiveRoundedFloat
from pydantic import BaseModel, Field


class DroughtIntensity(Intensity):
    duration_months: PositiveRoundedFloat
    severity: PositiveRoundedFloat


class ReturnPeriod(BaseModel):
    intensity: DroughtIntensity
    vulnerability: type(NOT_IMPLEMENTED_PLACEHOLDER)


class DroughtRiskAssessment(BaseModel):
    return_period_20y: ReturnPeriod
    return_period_100y: ReturnPeriod
    return_period_200y: ReturnPeriod


class AverageAnnualLoss(BaseModel):
    value: type(NOT_IMPLEMENTED_PLACEHOLDER)
    national_average: type(NOT_IMPLEMENTED_PLACEHOLDER)
    regional_average: type(NOT_IMPLEMENTED_PLACEHOLDER)


class OutputSchema(BaseModel):
    address: str | None
    lat: Annotated[float, Field(ge=-90, le=90)]
    lon: Annotated[float, Field(ge=-180, le=180)]
    drought_risk_assessment: DroughtRiskAssessment
    risk_index: type(NOT_IMPLEMENTED_PLACEHOLDER)
    average_annual_loss: AverageAnnualLoss
    hazard_index: type(NOT_IMPLEMENTED_PLACEHOLDER)
