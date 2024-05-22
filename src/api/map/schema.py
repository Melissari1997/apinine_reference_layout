from typing import Dict, List

from common.input_schema import LatLonSchema
from common.status_codes import StatusCodes
from pydantic import BaseModel, conint


class MapBaselineInputSchema(LatLonSchema):
    layer: str

    @staticmethod
    def get_error_msg() -> str:
        return StatusCodes.QUERYSTRING_ERROR[1]


class MapRCPInputSchema(LatLonSchema):
    year: conint(gt=0)
    layer: str

    @staticmethod
    def get_error_msg() -> str:
        return StatusCodes.QUERYSTRING_ERROR_RCP[1]


class GeoJSONSchema(BaseModel):
    type: str
    metadata: Dict
    features: List
