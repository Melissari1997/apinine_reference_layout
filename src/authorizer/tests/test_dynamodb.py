import boto3
from authorizer.implementations.dynamodb import DynamoKeyDB
from moto import mock_aws


class TestDynamoDB:
    def init_populated_dynamodb(self, create_table_query, create_write_batch_query):
        client = boto3.client("dynamodb")
        client.create_table(**create_table_query)
        client.batch_write_item(**create_write_batch_query)

    def test_query_by_key(
        self, create_table_query, create_write_batch_query, table_name, result_set, pk
    ):
        with mock_aws():
            self.init_populated_dynamodb(create_table_query, create_write_batch_query)
            dynamodb = DynamoKeyDB(table_name)
            result = dynamodb.query_by_key(pk)["Items"]

            want = sorted(result_set, key=lambda x: x["SK"]["S"])
            got = sorted(result, key=lambda x: x["SK"]["S"])

            assert got == want

    def test_query_by_key_wrong_pk(
        self, create_table_query, create_write_batch_query, table_name
    ):
        with mock_aws():
            self.init_populated_dynamodb(create_table_query, create_write_batch_query)
            dynamodb = DynamoKeyDB(table_name)
            got = dynamodb.query_by_key("wrongpartitionkey")["Items"]

            want = []
            assert got == want

    def test_update_last_accessed(
        self, create_table_query, create_write_batch_query, table_name, pk
    ):
        with mock_aws():
            self.init_populated_dynamodb(create_table_query, create_write_batch_query)
            dynamodb = DynamoKeyDB(table_name)
            want_before_update, want_after_update = "0", "10000000"
            result_before = dynamodb.query_by_key(pk)["Items"]
            assert [
                item.get("last_access")["N"]
                for item in result_before
                if "last_access" in item
            ][0] == want_before_update

            hash_key = [
                item["PutRequest"]["Item"]["SK"]["S"]
                for item in create_write_batch_query["RequestItems"][table_name]
                if item["PutRequest"]["Item"]["PK"]["S"] == pk
                and item["PutRequest"]["Item"]["SK"]["S"].startswith("KEY#")
            ][0]

            dynamodb.update_last_accessed(want_after_update, pk, hash_key)
            result_after_update = dynamodb.query_by_key(pk)["Items"]
            got = [
                item.get("last_access")["N"]
                for item in result_after_update
                if "last_access" in item
            ][0]
            assert got == want_after_update

    def test_update_last_access_wrong_key(
        self, create_table_query, create_write_batch_query, result_set, table_name, pk
    ):
        with mock_aws():
            # I do not want to perform any update because the key is wrong
            # No new item should be created before_update == after_update
            self.init_populated_dynamodb(create_table_query, create_write_batch_query)
            dynamodb = DynamoKeyDB(table_name)

            want = sorted(result_set, key=lambda x: x["SK"]["S"])

            timestamp = 25000
            dynamodb.update_last_accessed(timestamp, pk, "wrong_hash")
            items = dynamodb.dynamodb_client.scan(TableName=table_name)

            got = sorted(items["Items"], key=lambda x: x["SK"]["S"])

            assert want == got
