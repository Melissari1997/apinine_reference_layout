from typing import Annotated

from pydantic import BaseModel, Field

PositiveInt = Annotated[int, Field(gt=0)]
PositiveFloat = Annotated[float, Field(ge=0)]
Probability = Annotated[float, Field(ge=0, le=1)]


class Intensity(BaseModel):
    pass


class FloodIntensity(Intensity):
    water_height: PositiveFloat


class ReturnPeriod(BaseModel):
    intensity: FloodIntensity
    vulnerability: Probability


class FloodRiskAssessment(BaseModel):
    return_period_20y: ReturnPeriod
    return_period_100y: ReturnPeriod
    return_period_200y: ReturnPeriod


class OutputSchema(BaseModel):
    address: str | None
    flood_risk_assessment: FloodRiskAssessment
    risk_index: PositiveInt
    average_annual_loss: Probability
