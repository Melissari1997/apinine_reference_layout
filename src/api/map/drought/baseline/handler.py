import os

from aws_lambda_powertools import Logger, Tracer
from common.parse_env import BaselineEnvParser
from common.response import handle_response
from drought.layer_range import drought_layer_range
from handler import handler as drought_handler
from schema import GeoJSONSchema, MapBaselineInputSchema

logger = Logger()
tracer = Tracer()


@handle_response(validate_schema=GeoJSONSchema)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: dict = None) -> dict:
    envparser = BaselineEnvParser(environ=os.environ)
    return drought_handler(
        event=event,
        context=context,
        layer_to_range=drought_layer_range,
        env_parser=envparser,
        model=MapBaselineInputSchema,
    )
