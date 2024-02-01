from datetime import datetime

import argon2
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
