from datetime import datetime

import argon2
import boto3
import pytest


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
def create_table_query():
    return {
        "TableName": "apinine-api-key",
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
def create_write_batch_query():
    return {
        "RequestItems": {
            "apinine-api-key": [
                {
                    "PutRequest": {
                        "Item": {
                            "PK": {"S": "USER#user"},
                            "SK": {
                                "S": "KEY#$argon2id$v=19$m=32768,t=1,p=2$fQ3pbbOGdBeqJ+L2+tS7hA$eFWUm7SDdy/jWOaAnbm+3lMyFXucId4zxiKaHzkspXw"
                            },
                            "last_access": {"N": "0"},
                            "created_at": {"N": "1706803927"},
                            "expires_at": {"N": "1706903927"},
                        },
                    }
                },
                {
                    "PutRequest": {
                        "Item": {
                            "PK": {"S": "USER#user"},
                            "SK": {"S": "PERMISSION#GET#/flood/rcp85"},
                        }
                    }
                },
                {
                    "PutRequest": {
                        "Item": {
                            "PK": {"S": "USER#user"},
                            "SK": {"S": "PERMISSION#GET#/drought"},
                        }
                    }
                },
            ]
        }
    }


@pytest.fixture
def create_and_populate_table(create_table_query, create_write_batch_query):
    client = boto3.client("dynamodb")
    client.create_table(**create_table_query)

    client.batch_write_item(create_write_batch_query)
