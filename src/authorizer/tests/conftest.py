from datetime import datetime

import argon2
import boto3
import pytest
from moto import mock_aws


@pytest.fixture(scope="function")
def dynamo_query_item():
    key = "myuserpart:mysecretpart"
    user, secret = key.split(":")
    hashed_secret = argon2.PasswordHasher(
        time_cost=1, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16
    ).hash(secret)
    now = datetime.now().timestamp()

    yield {
        "key": key,
        "user": user,
        "secret": secret,
        "hashed_secret": hashed_secret,
        "now": now,
    }


@pytest.fixture
def create_table_query(table_name):
    return {
        "TableName": table_name,
        "KeySchema": [
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        "BillingMode": "PAY_PER_REQUEST",
        "AttributeDefinitions": [
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
        ],
    }


@pytest.fixture
def pk():
    return "USER#user"


@pytest.fixture
def table_name():
    return "test-table-key"


@pytest.fixture
def create_write_batch_query():
    def _create_write_batch_query(
        pk="USER#user",
        table_name="test-table-key",
        now=datetime.now().timestamp(),
        expires=datetime.now().timestamp() + 10,
    ):
        return {
            "RequestItems": {
                table_name: [
                    {
                        "PutRequest": {
                            "Item": {
                                "PK": {"S": pk},
                                "SK": {
                                    "S": "KEY#$argon2id$v=19$m=32768,t=1,p=2$fQ3pbbOGdBeqJ+L2+tS7hA$eFWUm7SDdy/jWOaAnbm+3lMyFXucId4zxiKaHzkspXw"
                                },
                                "last_access": {"N": "0"},
                                "created_at": {"N": str(int(now))},
                                "expires_at": {"N": str(int(expires))},
                            },
                        }
                    },
                    {
                        "PutRequest": {
                            "Item": {
                                "PK": {"S": pk},
                                "SK": {"S": "PERMISSION#GET#flood/rcp85"},
                            }
                        }
                    },
                    {
                        "PutRequest": {
                            "Item": {
                                "PK": {"S": pk},
                                "SK": {"S": "PERMISSION#GET#drought"},
                            }
                        }
                    },
                    {
                        "PutRequest": {
                            "Item": {
                                "PK": {"S": pk},
                                "SK": {"S": "ORG#terna"},
                            }
                        }
                    },
                ]
            }
        }

    return _create_write_batch_query


@pytest.fixture
def result_set():
    def _result_set(items, table_name="test-table-key"):
        return [
            request["PutRequest"]["Item"]
            for request in items["RequestItems"][table_name]
        ]

    return _result_set


@pytest.fixture
def populated_dynamodb(create_table_query, create_write_batch_query, table_name):
    with mock_aws():
        client = boto3.client("dynamodb")
        client.create_table(**create_table_query)
        client.batch_write_item(**create_write_batch_query)
        yield {"client": client, "table_name": table_name}
