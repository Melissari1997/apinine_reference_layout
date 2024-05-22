from typing import Dict, List

from common.input_schema import LatLonSchema
from pydantic import BaseModel, conint


class MapBaselineInputSchema(LatLonSchema):
    layer: str


class MapRCPInputSchema(LatLonSchema):
    year: conint(gt=0)
    layer: str


class GeoJSONSchema(BaseModel):
    type: str
    metadata: Dict
    features: List
