from typing import Dict, Tuple

from aws_lambda_powertools import Logger, Tracer
from bream.image import raster2 as brast
from cache import cache  # noqa: F401
from common.env_parser import EnvParser
from common.event_parser import parse_aws_event
from main import main
from map_converter import GeoJSONConverter
from map_reader import BreamMapReader
from schema import MapBaselineInputSchema, MapRCPInputSchema

logger = Logger()
tracer = Tracer()

EDGE_LENGTH_M = 600


def handler(
    event: dict,
    context: dict,
    layer_to_range: Dict[str, Tuple[float, float]],
    env_parser: EnvParser,
    model: MapBaselineInputSchema | MapRCPInputSchema,
) -> dict:

    filename, validated_event = parse_aws_event(
        event=event, env_parser=env_parser, model=model
    )

    global cache
    map_reader = BreamMapReader(cache=cache)
    map_converter = GeoJSONConverter()

    box_3035 = brast.MakeBox.from_point_and_size(
        coords=(validated_event.lon, validated_event.lat),
        coords_crs=4326,
        output_crs=3035,
        width=EDGE_LENGTH_M,
        height=EDGE_LENGTH_M,
    )
    response = main(
        filename=filename,
        box_3035=box_3035,
        layer=validated_event.layer,
        map_reader=map_reader,
        map_converter=map_converter,
        layer_to_range=layer_to_range,
    )

    logger.info(f"Returning response: {response}")
    return response
