from typing import List, Optional

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self

LAT_MIN, LAT_MAX = 27, 72
LON_MIN, LON_MAX = -22, 45


class QueryStringSchema(BaseModel):
    lat: float = Field(ge=LAT_MIN, le=LAT_MAX, default=None)
    lon: float = Field(ge=LON_MIN, le=LON_MAX, default=None)
    address: str = Field(min_length=1, default=None)

    @model_validator(mode="after")
    def check_address_or_lat_and_lon(self) -> Self:
        lat = self.lat
        lon = self.lon
        address = self.address
        # Allow only lat-lon or address
        correct = (address and not (lon or lat)) or ((lon and lat) and not address)
        if not correct:
            raise ValueError()
        return self


class QueryStringRCPSchema(QueryStringSchema):
    year: Optional[int]
    valid_years: List[int] = Field(exclude=True)

    @model_validator(mode="after")
    def check_year(self) -> Self:
        if self.year is not None and self.year not in self.valid_years:
            raise ValueError()
        return self


def validate_query_params(
    model: QueryStringSchema | QueryStringRCPSchema, params: dict
) -> dict:
    return model(**params)  # .model_dump()
