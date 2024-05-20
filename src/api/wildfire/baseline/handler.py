from aws_lambda_powertools import Logger, Tracer
from common.event_parser import parse_aws_event
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
    filename, address, lat, lon = parse_aws_event(event)

    response = main(
        filename=filename,
        address=address,
        lat=lat,
        lon=lon,
        geocoder=gmapsgeocoder,
        geodatareader=riogeoreader,
    )

    logger.info(f"Returning response: {response}")
    return response
