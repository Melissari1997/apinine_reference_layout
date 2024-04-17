import json
import os
from typing import Callable, Tuple

import boto3
import requests
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.utilities.typing import LambdaContext
from common.http_headers import response_headers
from interface import UserDB
from pydantic import ValidationError
from schema import EnvSchema
from userdb_paramstore import ParamStoreDB

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


def get_user_email(endpoint: str, auth_header: dict) -> str:
    response = requests.get(endpoint, headers=auth_header)
    response.raise_for_status()
    return response.json()["email"]


def get_userinfo_from_db(
    userinfo_endpoint: str, access_token: str, db: UserDB
) -> Tuple[dict, int]:
    auth_header = {"Authorization": access_token}

    try:
        id = get_user_email(endpoint=userinfo_endpoint, auth_header=auth_header)
    except requests.HTTPError as e:
        logger.info(f"Status code: {e.response.status_code}")
        return (e.response.status_code, {})

    user = db.query_user(id=id)
    if user is None:
        return (404, {})

    return (200, user)


@validate_env
def lambda_handler(event: dict, context: dict = None) -> dict:
    userinfo_endpoint = os.environ.get("URL_USERINFO")
    user_db_param = os.environ.get("USER_DB_PARAMETER_NAME")
    region_name = os.environ.get("SSM_PARAMETER_STORE_REGION", "eu-central-1")

    # SSM Parameter Store
    client_parameter_store = boto3.client("ssm", region_name=region_name)
    db = ParamStoreDB(client=client_parameter_store, parameter_name=user_db_param)
    access_token = event["headers"]["Authorization"].removeprefix("Bearer ")

    status_code, body = get_userinfo_from_db(
        userinfo_endpoint=userinfo_endpoint, access_token=access_token, db=db
    )

    response = {
        "body": json.dumps(body),
        "statusCode": status_code,
        "headers": response_headers,
    }

    return response
