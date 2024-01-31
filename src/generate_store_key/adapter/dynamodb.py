import datetime

import boto3
from botocore.exceptions import ClientError
from domain.key import KeyRepository


class DynamoDBKey(KeyRepository):
    def __init__(self):
        self.dynamodb_client = boto3.client("dynamodb")
        self.error_help_strings = {
            # Operation specific errors
            "ConditionalCheckFailedException": "Condition check specified in the operation failed, review and update the condition check before retrying",
            "TransactionConflictException": "Operation was rejected because there is an ongoing transaction for the item, generally safe to retry with exponential back-off",
            "ItemCollectionSizeLimitExceededException": "An item collection is too large, you're using Local Secondary Index and exceeded size limit of items per partition key."
            + " Consider using Global Secondary Index instead",
            # Common Errors
            "InternalServerError": "Internal Server Error, generally safe to retry with exponential back-off",
            "ProvisionedThroughputExceededException": "Request rate is too high. If you're using a custom retry strategy make sure to retry with exponential back-off."
            + "Otherwise consider reducing frequency of requests or increasing provisioned capacity for your table or secondary index",
            "ResourceNotFoundException": "One of the tables was not found, verify table exists before retrying",
            "ServiceUnavailable": "Had trouble reaching DynamoDB. generally safe to retry with exponential back-off",
            "ThrottlingException": "Request denied due to throttling, generally safe to retry with exponential back-off",
            "UnrecognizedClientException": "The request signature is incorrect most likely due to an invalid AWS access key ID or secret key, fix before retrying",
            "ValidationException": "The input fails to satisfy the constraints specified by DynamoDB, fix input before retrying",
            "RequestLimitExceeded": "Throughput exceeds the current throughput limit for your account, increase account level throughput before retrying",
        }

    def save_key_and_permission(self, hashed_key, permissions, organization, user):
        now = datetime.datetime.now()
        expiration_interval = datetime.timedelta(days=1000)
        expiration_date = now + expiration_interval

        hash_secret_string = f"KEY#{hashed_key}"
        user_pk = f"USER#{user}"

        key_item = {
            "TableName": "apinine_api_key",
            "Item": {
                "PK": {"S": user_pk},
                "SK": {"S": hash_secret_string},
                "last_access": {"N": str(int(now.timestamp()))},
                "created_at": {"N": str(int(now.timestamp()))},
                "expires_at": {"N": str(int(expiration_date.timestamp()))},
            },
        }

        permissions_items = []
        for perm in permissions:
            escaped_perm = f"/{perm}/"
            permissions_items.append(
                {
                    "PutRequest": {
                        "Item": {
                            "PK": {"S": user_pk},
                            "SK": {"S": f"PERMISSION#GET#{escaped_perm}"},
                        }
                    }
                }
            )

        batch_operations = [
            {"PutRequest": {"Item": key_item["Item"]}},
            {
                "PutRequest": {
                    "Item": {
                        "PK": {"S": user_pk},
                        "SK": {"S": f"ORG#{organization}"},
                    }
                }
            },
        ] + permissions_items

        batch_items = {"apinine_api_key": batch_operations}

        self.execute_batch_write_items(batch_items=batch_items)

    def execute_put_item(self, item):
        try:
            self.dynamodb_client.put_item(**item)
            print("Successfully put item.")
            # Handle response
        except ClientError as error:
            self.handle_error(error)
        except BaseException as error:
            print(f"Unknown error while putting item: {error}")

    def execute_batch_write_items(self, batch_items):
        try:
            self.dynamodb_client.batch_write_item(RequestItems=batch_items)
            print("Successfully put items.")
            # Handle response
        except ClientError as error:
            self.handle_error(error)
        except BaseException as error:
            print(f"Unknown error while putting items: {error}")

    def handle_error(self, error):
        error_code = error.response["Error"]["Code"]
        error_message = error.response["Error"]["Message"]

        error_help_string = self.error_help_strings[error_code]

        print(f"[{error_code}] {error_help_string}. Error message: {error_message}")
