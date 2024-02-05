import os

from aws_lambda_powertools import Logger  # , Tracer
from implementations.db_authenticator import DBAuthenticator
from implementations.dynamodb import DynamoKeyDB
from interfaces import Authenticator, KeyDB

logger = Logger()


def generate_policy(effect, resources):
    # Generate an IAM policy based on the effect (Allow/Deny) and the resource
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


def exception_handler_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.info(str(e))
        raise Exception("Unauthorized")

    return wrapper


@exception_handler_decorator
def authenticate_api_key(table_name, key, method_arn):
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
def handler(event, context):
    api_key = event["headers"]["x-api-key"]
    method_arn = event["methodArn"]
    table_name = os.environ.get("TABLE_NAME", "apinine_api_key")

    logger.info(f"Starting authorizer on method {method_arn}")

    return authenticate_api_key(
        table_name=table_name, key=api_key, method_arn=method_arn
    )
