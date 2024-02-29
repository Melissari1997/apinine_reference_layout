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


def validate_query_params(params: dict) -> dict:
    return QueryStringSchema(**params).model_dump()
