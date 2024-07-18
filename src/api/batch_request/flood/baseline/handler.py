import os

from aws_lambda_powertools import Logger, Tracer
from common.event_parser import parse_aws_event_body
from common.parse_env import BaselineEnvParser
from common.response import handle_response
from main import main
from schema import BatchRequestBodySchema, BatchRequestOutputSchema

logger = Logger()
tracer = Tracer()


@handle_response(validate_schema=BatchRequestOutputSchema)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: dict = None) -> dict:
    envparser = BaselineEnvParser(environ=os.environ)
    filename, validated_input = parse_aws_event_body(
        event=event, env_parser=envparser, model=BatchRequestBodySchema
    )
    bucket_name = os.environ["S3_BUCKET_NAME"]

    # Extract validated list of positions and convert to dictionary
    locations = [model.model_dump() for model in validated_input.locations]

    return main(
        filename=filename,
        locations=locations,
        bucket_name=bucket_name,
        body=event["body"].encode(),
    )
