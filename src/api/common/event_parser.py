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
