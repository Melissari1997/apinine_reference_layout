from authorizer.implementations.db_authenticator import DBAuthenticator
from authorizer.implementations.dynamodb import DynamoKeyDB
from aws_lambda_powertools import Logger  # , Tracer
from interfaces import Authenticator, KeyDB

logger = Logger()
# tracer = Tracer()
# import logging


# logger = logging.getLogger()


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


def authenticate_api_key(key, method_arn):
    dynamo_keydb: KeyDB = DynamoKeyDB()
    authenticator: Authenticator = DBAuthenticator(key_db=dynamo_keydb)

    logger.info("Checking API key")
    # This checks the key existence and expiration
    permissions = authenticator.authorize(key)
    logger.info(f"Found following permissions: {permissions}")

    # TODO: combine permissions with method_arn
    resources = method_arn

    policy = generate_policy("Allow", resources)

    logger.info(f"Generated policy: {policy}")
    return policy


@logger.inject_lambda_context
# @tracer.capture_lambda_handler
def handler(event, context):
    logger.info(f"event: {event}")
    logger.info(f"context: {context}")

    api_key = event["headers"]["x-api-key"]
    method_arn = event["methodArn"]

    return authenticate_api_key(key=api_key, method_arn=method_arn)


if __name__ == "__main__":
    handler(
        event={
            "headers": {"x-api-key": "mykey"},
            "httpMethod": "GET",
            "methodArn": "myMethodArn",
            "requestContext": {"path": "/wildfire"},
        },
        context={},
    )
