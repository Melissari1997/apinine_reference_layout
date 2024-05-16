import json
import os
from typing import Dict, Tuple

from aws_lambda_powertools import Logger, Tracer
from cache import cache  # noqa: F401
from main import main
from map_converter import GeoJSONConverter
from map_reader import BreamMapReader
from schema import MapInputSchema

logger = Logger()
tracer = Tracer()


def handler(
    event: dict, context: dict, layer_to_range: Dict[str, Tuple[float, float]]
) -> dict:
    geotiff_json = os.environ.get("GEOTIFF_JSON")

    if not geotiff_json:
        raise ValueError("Missing env var GEOTIFF_JSON")

    try:
        geotiff_list = json.loads(geotiff_json)
    except json.JSONDecodeError:
        raise ValueError(f"Variable is not a valid JSON: {geotiff_json}") from None

    event = event.get("queryStringParameters", {})

    validated_event = MapInputSchema(**event)
    if validated_event.year is not None:
        filename = next(
            entry["path"]
            for entry in geotiff_list
            if entry["year"] == str(validated_event.year)
        )
    else:
        filename = geotiff_list[0]["path"]

    global cache
    map_reader = BreamMapReader(cache=cache)
    map_converter = GeoJSONConverter()
    response = main(
        filename=filename,
        lat=validated_event.lat,
        lon=validated_event.lon,
        layer=validated_event.layer,
        map_reader=map_reader,
        map_converter=map_converter,
        layer_to_range=layer_to_range,
    )

    logger.info(f"Returning response: {response}")
    return response
