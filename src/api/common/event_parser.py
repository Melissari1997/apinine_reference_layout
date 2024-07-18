import json

from aws_lambda_powertools import Logger
from pydantic import BaseModel, ValidationError

from .parse_env import EnvParser

logger = Logger()


def parse_aws_event(event: dict, env_parser: EnvParser, model: BaseModel) -> BaseModel:
    query_params = event.get("queryStringParameters")
    if query_params is None:
        query_params = {}

    # Validate the query parameters
    logger.info(f"Validating query parameters: {query_params}")
    try:
        validated_params = model(**query_params)
    except ValidationError as ve:
        # Raise an error with a message specific for that schema
        raise ve.from_exception_data(
            title=model.get_error_msg(), line_errors=ve.errors()
        ) from None

    # Use the environment and optionally the query parameters to get the tiff filename
    filename = env_parser.get_filename(**validated_params.model_dump())

    return filename, validated_params


def parse_aws_event_body(
    event: dict, env_parser: EnvParser, model: BaseModel
) -> tuple[str, BaseModel]:
    if (event["body"]) and (event["body"] is not None):
        body = json.loads(event["body"])

    # Validate the query parameters
    logger.info(f"Validating body: {body}")
    try:
        validated_params = model(**body)
    except ValidationError as ve:
        # Raise an error with a message specific for that schema
        raise ve.from_exception_data(
            title=model.get_error_msg(), line_errors=ve.errors()
        ) from None

    filename = env_parser.get_filename()

    return filename, validated_params


# TODO: unify the above functions so that the pydantic schemas also validate the meta-keys "queryStringParameters" and "body"
# This way every schema can validate either the query params or the body and we can use a single function

# The above division between 'parse_aws_event' and 'parse_aws_event_body' is just temporary.
# Here I leave a different implementation to be added as refactoring after batch request implementation will be over
# This will involve changes in a significant number of files, so I prefer to do it in a next increment


# event_keys_to_parse = ["queryStringParameters", "body"]


# def parse_aws_event(event: dict, env_parser: EnvParser, model: BaseModel) -> BaseModel:
#     event = {key: event[key] for key in event if key in event_keys_to_parse}

#     # Validate query and/or body parameters
#     logger.info(f"Validating event: {event}")
#     try:
#         validated_params = model(**event)
#     except ValidationError as ve:
#         # Raise an error with a message specific for that schema
#         raise ve.from_exception_data(
#             title=model.get_error_msg(), line_errors=ve.errors()
#         ) from None

#     # Use the environment and optionally the query parameters to get the tiff filename
#     filename = env_parser.get_filename(**validated_params.model_dump())

#     return filename, validated_params
