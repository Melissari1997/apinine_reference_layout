import os
from typing import Callable

from aws_lambda_powertools import Logger
from implementations.db_authenticator import DBAuthenticator
from implementations.dynamodb import DynamoKeyDB
from interfaces import Authenticator, KeyDB

logger = Logger()


def generate_policy(effect: str, resources: list[str]) -> dict:
    """Generate an IAM policy based on the effect (Allow/Deny) and the resource

    Parameters
    ----------
    effect : str
        'Allow' or 'Deny' literals are valid.
        We only set 'Allow' policies since 'Deny' is the default behaviour.
    resources : list[str]
        List of resources to apply the effect to.
        This is usually the ARN of the invoked API Gateway endpoint.

    Returns
    -------
    dict
        IAM policy as dictionary, allowing or denying the access to the endpoint.
    """
    policy = {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resources,
                }
            ],
        },
    }

    return policy


def exception_handler(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.info(str(e))
        # Exception("Unauthorized") is the suggested way to return 401 to the client
        raise Exception("Unauthorized")

    return wrapper


@exception_handler
def authenticate_api_key(table_name: str, key: str, method_arn: str) -> dict:
    """Generate an IAM policy for the specified key and resource.

    Query the backend DynamoDB's 'table_name' table, get a list of
    permissions associated with provided API key

    Parameters
    ----------
    table_name : str
        Name of DynamoDB table.
    key : str
        API key to check.
    method_arn : str
        ARN of the invoked API Gateway endpoint.

    Returns
    -------
    policy: dict
        IAM policy allowing or denying the access to the endpoint.
    """
    dynamo_keydb: KeyDB = DynamoKeyDB(table_name=table_name)
    authenticator: Authenticator = DBAuthenticator(key_db=dynamo_keydb)

    logger.info("Checking API key")
    # This checks the key existence and expiration
    # Long paths flood/rcp85/another/path may increase the splitted list lenght
    # I am interested only in the 3rd and 4th elemement of the split
    _, _, method, resource = method_arn.split("/", 3)
    is_allowed = authenticator.authorize(key, method, resource)
    logger.info(f"Found following permissions: {is_allowed}")

    permitted_resources = [method_arn] if is_allowed else []
    policy = generate_policy("Allow", permitted_resources)

    logger.info(f"Generated policy: {policy}")
    return policy


@logger.inject_lambda_context
def handler(event: dict, context: dict) -> dict:
    """Lambda handler.

    This is the lambda entrypoint.

    Parameters
    ----------
    event : dict
        Data passed to the function upon execution.
    context : dict
        Provides information about the current execution environment.
        Currently is ignored.

    Returns
    -------
    dict
        IAM policy as dictionary, allowing or denying the access to the endpoint.
    """
    api_key = event["headers"]["x-api-key"]
    method_arn = event["methodArn"]
    table_name = os.environ.get("TABLE_NAME", "apinine_api_key")

    logger.info(f"Starting authorizer on method {method_arn}")

    return authenticate_api_key(
        table_name=table_name, key=api_key, method_arn=method_arn
    )
