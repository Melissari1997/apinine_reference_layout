from typing import Annotated

from common.errors import MissingDataError
from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator


def check_positive(f: float) -> float:
    if f < 0:
        raise MissingDataError
    return f


PositiveInt = Annotated[int, Field(ge=0)]
PositiveFloat = Annotated[float, AfterValidator(check_positive)]
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


class AverageAnnualLoss(BaseModel):
    value: PositiveFloat
    national_average: PositiveFloat


class OutputSchema(BaseModel):
    address: str | None
    lat: PositiveFloat
    lon: PositiveFloat
    flood_risk_assessment: FloodRiskAssessment
    risk_index: PositiveInt
    average_annual_loss: AverageAnnualLoss
