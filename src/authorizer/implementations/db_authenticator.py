from datetime import datetime

import argon2
from interfaces import Authenticator, KeyDB


class DBAuthenticator(Authenticator):
    def __init__(self, key_db: KeyDB) -> None:
        self.password_hasher = argon2.PasswordHasher(
            time_cost=1, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16
        )
        self.key_db = key_db

    def authorize(self, key: str, method: str, resource: str):
        """
        Inputs:
            - key: string e.g. myuser:mysecret
            - method: string e.g GET (upper)
            - resource: string e.g. /flood/rcp85

        Return an array of the type ["GET#/wildfire/", "GET#/flood/", ...]
        raise Exception("Unauthorized") is the suggested way to return 401 to the client
        """

        # Verify the key is in the correct format user:secret
        splitted = key.split(":")
        if len(splitted) != 2:
            print("INVALIDKEYFORMAT - Invalid key format")
            raise Exception("Unauthorized")

        user, secret = splitted
        pk_key_item = f"USER#{user}"
        result = self.key_db.query_by_key(pk_key_item)  # noqa: F841

        if result["Count"] == 0:
            raise Exception("Unauthorized")  # Return immediately

        now_ts = datetime.now().timestamp()
        # Get the key item (PK and SK === KEY#....)
        # Here we have found the items in the DB and
        # we do not support multiple KEYs per user
        try:
            key_item = [
                x
                for x in result["Items"]
                if x["PK"]["S"] == pk_key_item
                and x["SK"]["S"].startswith("KEY#")
                and self.password_hasher.verify(
                    x["SK"]["S"].removeprefix("KEY#"), secret
                )
            ][0]
        except argon2.exceptions.InvalidHashError:
            print(
                f"HASHERROR - the hash or the hasher have been changed. User {pk_key_item}"
            )
            # silcence ruff because this exception is force by AWS
            raise Exception("Unauthorized")  # noqa: B904
        except IndexError:
            print(
                f"NOKEYSKERROR - no KEY sort key found. data may be inconsistent. User {pk_key_item}"
            )
            # silcence ruff because this exception is force by AWS
            raise Exception("Unauthorized")  # noqa: B904

        if int(key_item["expires_at"]["N"]) < now_ts:
            raise Exception("Unauthorized")  # Return immediately

        self.key_db.update_last_accessed(last_accessed_ts=now_ts)
        method_resource = f"{method}#{resource}"  # this is how it is saved on our DB
        # We do not support PERMISSION* (wildcard)
        permissions = [
            x["SK"]["S"].removeprefix("PERMISSION#")
            for x in result["Items"]
            if x["PK"]["S"] == pk_key_item
            and x["SK"]["S"].startswith(f"PERMISSION#{method_resource}")
        ]

        return len(permissions) > 0
