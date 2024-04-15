import os
import urllib.parse
from typing import Callable

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError
from schema import EnvSchema

logger = Logger()
tracer = Tracer()


@lambda_handler_decorator
def validate_env(
    handler: Callable[[dict, LambdaContext], dict], event: dict, context: LambdaContext
) -> dict:
    try:
        EnvSchema(**os.environ)
    except (ValidationError, TypeError) as ex:
        raise ValueError(f"Failed to load env variables: {str(ex)}") from ex
    return handler(event, context)


@validate_env
def lambda_handler(event: dict, context: dict = None) -> dict:
    url = os.environ.get("URL", "")
    app_client_id = os.environ.get("APP_CLIENT_ID", "")
    callback_uri = event.get("callback_uri", os.environ.get("CALLBACK_URI", ""))

    cognito_ui_uri = f"{url}?response_type=code&client_id={app_client_id}&scope=email+openid&redirect_uri={urllib.parse.quote_plus(callback_uri)}"

    response = {"statusCode": "302", "headers": {"Location": cognito_ui_uri}}
    return response
