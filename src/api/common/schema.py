from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator

from .errors import MissingDataError

# TODO: move rounding logic to the components producing the lookup
DECIMAL_PLACES = 4
NOT_IMPLEMENTED_PLACEHOLDER = "Not implemented"


def check_positive(f: float) -> float:
    if f < 0:
        raise MissingDataError
    return f


def round_float(f: float) -> float:
    return round(f, DECIMAL_PLACES)


class Intensity(BaseModel):
    pass


Probability = Annotated[float, Field(ge=0, le=1), AfterValidator(round_float)]
PositiveFloat = Annotated[float, AfterValidator(check_positive)]
PositiveRoundedFloat = Annotated[PositiveFloat, AfterValidator(round_float)]
