import boto3
from authorizer.interfaces import KeyDB
from botocore.exceptions import ClientError


class DynamoKeyDB(KeyDB):
    def __init__(self) -> None:
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

    def query_by_key(self, pk: str):
        query = self.create_query_input(pk)
        result = self.execute_query(query)
        return result["Items"]

    def update_last_accessed(self, last_accessed_ts: int, hash_key: str):
        update_item = {
            "TableName": "apinine_api_key",
            "Key": {"PK": {"S": hash_key}, "SK": {"S": hash_key}},
            "UpdateExpression": "SET #75040 = :75040",
            "ExpressionAttributeNames": {"#75040": "last_access"},
            "ExpressionAttributeValues": {":75040": {"N": str(last_accessed_ts)}},
        }

        self.execute_update_item(update_item)

    def execute_update_item(self, update_item):
        try:
            self.dynamodb_client.update_item(**update_item)
            print("Successfully updated item.")
            # Handle response
        except ClientError as error:
            self.handle_error(error)
        except BaseException as error:
            print("Unknown error while updating item: " + error)

    def create_query_input(self, pk: str):
        return {
            "TableName": "apinine_api_key",
            "KeyConditionExpression": "#e14e0 = :e14e0",
            "ExpressionAttributeNames": {"#e14e0": "PK"},
            "ExpressionAttributeValues": {":e14e0": {"S": pk}},
        }

    def execute_query(self, item):
        try:
            response = self.dynamodb_client.query(**item)
            print("Query successful.")
            # Handle response
        except ClientError as error:
            self.handle_error(error)
        except BaseException as error:
            print("Unknown error while querying: " + error)

        return response

    def handle_error(self, error):
        error_code = error.response["Error"]["Code"]
        error_message = error.response["Error"]["Message"]

        error_help_string = self.error_help_strings[error_code]

        print(f"[{error_code}] {error_help_string}. Error message: {error_message}")
