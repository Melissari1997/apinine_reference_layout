import json
import os
from typing import Callable

import requests
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
    app_client_id = os.environ.get("APP_CLIENT_ID", "")
    callback_uri = os.environ.get("CALLBACK_URI", "")
    url = os.environ.get("URL", "")

    code = event.get("queryStringParameters", {}).get("code", "")

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=authorization_code&client_id={app_client_id}&code={code}&redirect_uri={callback_uri}"

    r = requests.post(url, headers=headers, data=data, timeout=5)

    status_code = r.status_code
    logger.info(f"status code: {r.status_code}")
    body = r.json()
    response = {
        "body": json.dumps(body),
        "statusCode": status_code,
    }
    return response