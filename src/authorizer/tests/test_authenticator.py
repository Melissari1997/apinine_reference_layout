import argon2
from implementations.db_authenticator import DBAuthenticator
from interfaces import KeyDB


class KeyDBMock(KeyDB):
    def __init__(self, test_obj) -> None:
        self.key = test_obj["key"]
        self.hashed_key = test_obj["hashed_key"]
        self.query_item = test_obj["query_item"]

    def query_by_key(self, key: str):
        return self.query_item

    def update_last_accessed(self, last_accessed_ts: int):
        pass


class TestAuthenticator:
    def test_authorize(self):
        key = "mykey"
        hashed_key = argon2.PasswordHasher(
            time_cost=1, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16
        ).hash(key)
        key_db_input = {
            "key": key,
            "hashed_key": hashed_key,
            "query_item": {
                "Count": 5,
                "Items": [
                    {
                        "PK": {
                            "S": f"KEY#{hashed_key}",
                        },
                        "SK": {
                            "S": f"KEY#{hashed_key}",
                        },
                        "last_access": {
                            "N": "0",
                        },
                        "created_at": {
                            "N": "100000",
                        },
                        "expires_at": {
                            "N": "101000",
                        },
                    },
                    {
                        "PK": {
                            "S": f"KEY#{hashed_key}",
                        },
                        "SK": {
                            "S": "PERMISSION#GET#/wildfire",
                        },
                    },
                    {
                        "PK": {
                            "S": f"KEY#{hashed_key}",
                        },
                        "SK": {
                            "S": "PERMISSION#GET#/flood",
                        },
                    },
                    {
                        "PK": {
                            "S": f"KEY#{hashed_key}",
                        },
                        "SK": {
                            "S": "PERMISSION#GET#/flood/rcp85",
                        },
                    },
                    {
                        "PK": {
                            "S": f"KEY#{hashed_key}",
                        },
                        "SK": {
                            "S": "ORG#TERNA",
                        },
                    },
                ],
            },
        }
        want = True
        mykeydbmock = KeyDBMock(key_db_input)
        got = DBAuthenticator(mykeydbmock).authorize(key, "GET", "/flood")

        assert got == want
