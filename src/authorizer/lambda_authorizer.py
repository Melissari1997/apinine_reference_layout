import logging

logger = logging.getLogger()
logger.setLevel("INFO")


def handler(event, context):
    logger.info(f"event: {event}")
    logger.info(f"context: {context}")

    # Extract api key from the event
    api_key = event["x-api-key"]

    # Perform authentication logic
    # Replace this with your actual authentication logic
    user_authenticated = authenticate_api_key(api_key)

    if user_authenticated:
        # If user is authenticated, generate IAM policy
        policy = generate_policy("Allow", event["methodArn"])
    else:
        # If user is not authenticated, deny access
        policy = generate_policy("Deny", event["methodArn"])

    return policy


def authenticate_api_key(token):
    # Replace this with your actual authentication logic
    # Example: Check if the token is valid or exists in a user database
    # Return True if authenticated, False otherwise
    return True


def generate_policy(effect, resource):
    # Generate an IAM policy based on the effect (Allow/Deny) and the resource
    policy = {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource,
                }
            ],
        },
    }

    return policy
