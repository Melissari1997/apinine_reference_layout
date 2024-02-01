from datetime import datetime

import argon2
import pytest
from implementations.db_authenticator import DBAuthenticator
from interfaces import KeyDB


class KeyDBMock(KeyDB):
    def __init__(self, test_obj) -> None:
        self.key = test_obj["key"]
        splitted = self.key.split(":")
        # Pad always to length 2
        self.user, self.secret = splitted + [""] * (2 - len(splitted))
        self.hashed_key = test_obj["hashed_key"]
        self.user_pk = test_obj.get("user_pk", f"USER#{self.user}")
        self.created_at = test_obj["created_at"]
        self.expires_at = test_obj.get("expires_at", str(int(self.created_at) + 10))
        self.count = test_obj.get("count", -1)
        self.main_sk_prefix = test_obj.get("main_sk_prefix", "KEY#")

    def query_by_key(self, key: str):
        items = [
            {
                "PK": {
                    "S": self.user_pk,
                },
                "SK": {
                    "S": f"{self.main_sk_prefix}{self.hashed_key}",
                },
                "last_access": {
                    "N": "0",
                },
                "created_at": {
                    "N": self.created_at,
                },
                "expires_at": {
                    "N": self.expires_at,
                },
            },
            {
                "PK": {
                    "S": self.user_pk,
                },
                "SK": {
                    "S": "PERMISSION#GET#/wildfire",
                },
            },
            {
                "PK": {
                    "S": self.user_pk,
                },
                "SK": {
                    "S": "PERMISSION#GET#/flood",
                },
            },
            {
                "PK": {
                    "S": self.user_pk,
                },
                "SK": {
                    "S": "PERMISSION#GET#/flood/rcp85",
                },
            },
            {
                "PK": {
                    "S": self.user_pk,
                },
                "SK": {
                    "S": "ORG#TERNA",
                },
            },
        ]

        # Handle specific case count = 0
        return {
            "Count": len(items) if self.count else self.count,
            "Items": items if self.count else [],
        }

    def update_last_accessed(self, last_accessed_ts: int):
        pass


class TestAuthenticator:
    def test_authorize_happy_path(self):
        key = "myuserpart:mysecretpart"
        user, secret = key.split(":")
        hashed_secret = argon2.PasswordHasher(
            time_cost=1, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16
        ).hash(secret)

        now = datetime.now().timestamp()

        user_pk = f"USER#{user}"

        key_db_input = {
            "key": key,
            "hashed_key": hashed_secret,
            "user_pk": user_pk,
            "created_at": str(int(now)),
        }
        want = True
        mykeydbmock = KeyDBMock(key_db_input)
        got = DBAuthenticator(mykeydbmock).authorize(key, "GET", "/flood")

        assert got == want

    def test_expired_key(self):
        key = "myuserpart:mysecretpart"
        user, secret = key.split(":")
        hashed_secret = argon2.PasswordHasher(
            time_cost=1, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16
        ).hash(secret)

        now = datetime.now().timestamp()

        user_pk = f"USER#{user}"

        key_db_input = {
            "key": key,
            "hashed_key": hashed_secret,
            "user_pk": user_pk,
            "created_at": str(int(now)),
            "expires_at": "0",  # force expiration
        }
        wanted_exception = "Unauthorized"
        mykeydbmock = KeyDBMock(key_db_input)

        with pytest.raises(Exception, match=wanted_exception):
            DBAuthenticator(mykeydbmock).authorize(key, "GET", "/flood")

    def test_user_not_found(self, dynamo_query_item):
        key = dynamo_query_item["key"]

        user_pk = f'USER#{dynamo_query_item["user"]}'

        key_db_input = {
            "key": dynamo_query_item["key"],
            "hashed_key": dynamo_query_item["hashed_secret"],
            "user_pk": user_pk,
            "created_at": dynamo_query_item["now"],
            "count": 0,  # force it
        }

        wanted_exception = "Unauthorized"
        mykeydbmock = KeyDBMock(key_db_input)

        with pytest.raises(Exception, match=wanted_exception):
            DBAuthenticator(mykeydbmock).authorize(key, "GET", "/flood")

    def test_fail_hashed_key_verification(self, dynamo_query_item):
        """
        It might happen when:
            - the hasher in the script has different values from the hasher in the authorizer
            - someone modified the saved hash (KEY#....) in the DB
        """

        key = dynamo_query_item["key"]

        user_pk = f'USER#{dynamo_query_item["user"]}'

        key_db_input = {
            "key": dynamo_query_item["key"],
            "hashed_key": "failing_hash",  # pass wrong hash
            "user_pk": user_pk,
            "created_at": dynamo_query_item["now"],
        }

        mykeydbmock = KeyDBMock(key_db_input)

        # It always throw the same exception, but we write the error in the log
        wanted_exception = "Unauthorized"

        with pytest.raises(Exception, match=wanted_exception):
            DBAuthenticator(mykeydbmock).authorize(key, "GET", "/flood")

    def test_no_key_found_in_user(self, dynamo_query_item):
        # KEY#... missing in the Item
        """
        It might happen when:
            - the SORT key in the item USER(PK)-KEY(SK) does not begin with KEY or it is missing
                e.g. USER#awuw29 KEY#$argon2id.... is missing
        """

        key = dynamo_query_item["key"]

        user_pk = f'USER#{dynamo_query_item["user"]}'

        key_db_input = {
            "key": dynamo_query_item["key"],
            "hashed_key": dynamo_query_item["hashed_secret"],
            "user_pk": user_pk,
            "created_at": dynamo_query_item["now"],
            "main_sk_prefix": "WRONG#",
        }

        mykeydbmock = KeyDBMock(key_db_input)

        # It always throw the same exception, but we write the error in the log
        wanted_exception = "Unauthorized"

        with pytest.raises(Exception, match=wanted_exception):
            DBAuthenticator(mykeydbmock).authorize(key, "GET", "/flood")

    def test_wrong_key_format(self, dynamo_query_item):
        # key is not in the format user:secret

        user_pk = f'USER#{dynamo_query_item["user"]}'
        key = "mywrongrandomkey"  # do not take key from default valid values

        key_db_input = {
            "key": key,
            "hashed_key": dynamo_query_item["hashed_secret"],
            "user_pk": user_pk,
            "created_at": dynamo_query_item["now"],
        }

        mykeydbmock = KeyDBMock(key_db_input)
        wanted_exception = "Unauthorized"

        with pytest.raises(Exception, match=wanted_exception):
            DBAuthenticator(mykeydbmock).authorize(key, "GET", "/flood")

    def test_missing_permissions(self, dynamo_query_item):
        key = dynamo_query_item["key"]

        user_pk = f'USER#{dynamo_query_item["user"]}'

        key_db_input = {
            "key": dynamo_query_item["key"],
            "hashed_key": dynamo_query_item["hashed_secret"],
            "user_pk": user_pk,
            "created_at": dynamo_query_item["now"],
        }

        mykeydbmock = KeyDBMock(key_db_input)
        want = False
        got = DBAuthenticator(mykeydbmock).authorize(key, "GET", "/flood/invalid/path")

        assert want == got
