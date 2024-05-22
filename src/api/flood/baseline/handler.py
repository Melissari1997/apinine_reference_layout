import os

from aws_lambda_powertools import Logger, Tracer
from common.env_parser import BaselineEnvParser
from common.event_parser import parse_aws_event
from common.input_schema import RiskInputSchema
from common.response import handle_response
from geocoder.gmaps_geocoder import GMapsGeocoder
from main import main
from readgeodata.rasterioreader import RasterIOReader
from schema import OutputSchema

logger = Logger()
tracer = Tracer()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


@handle_response(validate_schema=OutputSchema)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: dict = None) -> dict:
    envparser = BaselineEnvParser(environ=os.environ)
    filename, validated_input = parse_aws_event(
        event=event, env_parser=envparser, model=RiskInputSchema
    )
    response = main(
        filename=filename,
        address=validated_input.address,
        lat=validated_input.lat,
        lon=validated_input.lon,
        geocoder=gmapsgeocoder,
        geodatareader=riogeoreader,
    )

    logger.info(f"Returning response: {response}")
    return response
