import os

from aws_lambda_powertools import Logger, Tracer
from common.env_parser import BaselineEnvParser
from common.event_parser import parse_aws_event
from common.input_schema import RiskInputSchema
from common.response import handle_response
from handler import handler as drought_handler
from schema import GeoJSONSchema

from .layer_range import drought_layer_range

logger = Logger()
tracer = Tracer()

envparser = BaselineEnvParser(environ=os.environ)


@handle_response(validate_schema=GeoJSONSchema)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: dict = None) -> dict:
    filename, validated_input = parse_aws_event(
        event=event, env_parser=envparser, model=RiskInputSchema
    )
    return drought_handler(
        event=event, context=context, layer_to_range=drought_layer_range
    )
