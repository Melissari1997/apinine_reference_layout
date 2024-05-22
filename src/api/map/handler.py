from typing import Dict, Tuple

from aws_lambda_powertools import Logger, Tracer
from cache import cache  # noqa: F401
from common.env_parser import EnvParser
from common.event_parser import parse_aws_event
from main import main
from map_converter import GeoJSONConverter
from map_reader import BreamMapReader
from schema import MapInputSchema

logger = Logger()
tracer = Tracer()


def handler(
    event: dict,
    context: dict,
    layer_to_range: Dict[str, Tuple[float, float]],
    envparser: EnvParser,
) -> dict:

    filename, validated_event = parse_aws_event(
        event=event, env_parser=envparser, model=MapInputSchema
    )

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
