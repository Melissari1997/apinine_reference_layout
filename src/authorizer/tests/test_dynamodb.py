import boto3
from authorizer.implementations.dynamodb import DynamoKeyDB
from moto import mock_aws


class TestDynamoDB:
    def init_populated_dynamodb(
        self, create_table_query, create_write_batch_query, table_name
    ):
        client = boto3.client("dynamodb")
        client.create_table(**create_table_query)
        client.batch_write_item(**create_write_batch_query)

    def test_query_by_key(
        self, create_table_query, create_write_batch_query, table_name, result_set, pk
    ):
        with mock_aws():
            self.init_populated_dynamodb(
                create_table_query, create_write_batch_query, table_name
            )
            dynamodb = DynamoKeyDB(table_name)
            result = dynamodb.query_by_key(pk)

            want = sorted(result_set, key=lambda x: x["SK"]["S"])
            got = sorted(result, key=lambda x: x["SK"]["S"])

            assert got == want
