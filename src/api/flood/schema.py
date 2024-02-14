from typing import Annotated

from common.errors import MissingDataError
from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator

# TODO: move rounding logic to the components producing the lookup
DECIMAL_PLACES = 4


def check_positive(f: float) -> float:
    if f < 0:
        raise MissingDataError
    return f


def round_float(f: float) -> float:
    return round(f, DECIMAL_PLACES)


PositiveInt = Annotated[int, Field(ge=0)]
PositiveFloat = Annotated[float, AfterValidator(check_positive)]
PositiveRoundedFloat = Annotated[PositiveFloat, AfterValidator(round_float)]
Probability = Annotated[float, Field(ge=0, le=1), AfterValidator(round_float)]


class Intensity(BaseModel):
    pass


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


class OutputSchema(BaseModel):
    address: str | None
    lat: Annotated[float, Field(ge=-90, le=90)]
    lon: Annotated[float, Field(ge=-180, le=180)]
    flood_risk_assessment: FloodRiskAssessment
    risk_index: PositiveInt
    average_annual_loss: AverageAnnualLoss
