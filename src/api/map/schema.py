from typing import Dict, List, Optional

from common.input_schema import LAT_MAX, LAT_MIN, LON_MAX, LON_MIN
from pydantic import BaseModel, Field


class MapInputSchema(BaseModel):
    lat: float = Field(ge=LAT_MIN, le=LAT_MAX)
    lon: float = Field(ge=LON_MIN, le=LON_MAX)
    layer: str
    year: Optional[int] = None


class GeoJSONSchema(BaseModel):
    type: str
    metadata: Dict
    features: List
