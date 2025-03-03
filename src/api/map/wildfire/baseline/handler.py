import os

from aws_lambda_powertools import Logger, Tracer
from common.parse_env import BaselineEnvParser
from common.response import handle_response
from handler import handler as wildfire_handler
from schema import GeoJSONSchema, MapBaselineInputSchema
from wildfire.layer_range import wildfire_layer_range

logger = Logger()
tracer = Tracer()


@handle_response(validate_schema=GeoJSONSchema)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: dict = None) -> dict:
    envparser = BaselineEnvParser(environ=os.environ)
    return wildfire_handler(
        event=event,
        context=context,
        layer_to_range=wildfire_layer_range,
        env_parser=envparser,
        model=MapBaselineInputSchema,
    )
