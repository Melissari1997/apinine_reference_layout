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


PositiveFloat = Annotated[float, AfterValidator(check_positive)]
PositiveRoundedFloat = Annotated[PositiveFloat, AfterValidator(round_float)]


class ReturnPeriod(BaseModel):
    duration_month: PositiveRoundedFloat
    severity: PositiveRoundedFloat


class DroughtRiskAssessment(BaseModel):
    return_period_2y: ReturnPeriod
    return_period_10y: ReturnPeriod
    return_period_30y: ReturnPeriod


class OutputSchema(BaseModel):
    address: str | None
    lat: Annotated[float, Field(ge=-90, le=90)]
    lon: Annotated[float, Field(ge=-180, le=180)]
    drought_risk_assessment: DroughtRiskAssessment
