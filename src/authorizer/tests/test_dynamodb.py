from implementations.dynamodb import DynamoKeyDB
from moto import mock_aws


class TestDynamoDB:
    @mock_aws
    def test_query_by_key(self, create_and_populate_table):
        dynamo_keydb = DynamoKeyDB()
        dynamo_keydb.query_by_key()
