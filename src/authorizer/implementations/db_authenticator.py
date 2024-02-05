import os
from datetime import datetime

import argon2
from aws_lambda_powertools import Logger
from interfaces import Authenticator, KeyDB

logger = Logger()


class DBAuthenticator(Authenticator):
    def __init__(self, key_db: KeyDB) -> None:
        """_summary_

        Args:
            key_db (KeyDB): _description_
        """
        time_cost = int(os.environ.get("HASHER_TIME_COST"))
        memory_cost = int(os.environ.get("HASHER_MEMORY_COST"))
        parallelism = int(os.environ.get("HASHER_PARALLELISM"))
        hash_len = int(os.environ.get("HASHER_HASH_LEN"))
        salt_len = int(os.environ.get("HASHER_SALT_LEN"))
        self.password_hasher = argon2.PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=hash_len,
            salt_len=salt_len,
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
        try:
            user, secret = key.split(":")
        except ValueError as ve:
            raise ValueError("INVALIDKEYFORMAT - Invalid key format") from ve

        logger.info(f"Found user {user}")

        pk_key_item = f"USER#{user}"
        result = self.key_db.query_by_key(pk_key_item)

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
        except argon2.exceptions.InvalidHashError as ihe:
            raise ValueError(
                f"HASHERROR - the hash or the hasher have been changed. User {pk_key_item}"
            ) from ihe
        except IndexError as ie:
            raise ValueError(
                f"NOKEYSKERROR - no KEY sort key found. data may be inconsistent. User {pk_key_item}"
            ) from ie

        if int(key_item["expires_at"]["N"]) < now_ts:
            raise ValueError(f"EXPIREDKEYERROR - key is expired. User {pk_key_item}")

        self.key_db.update_last_accessed(
            last_accessed_ts=now_ts,
            user=key_item["PK"]["S"],
            hash_key=key_item["SK"]["S"],
        )
        method_resource = f"{method}#{resource}"  # this is how it is saved on our DB
        # We do not support PERMISSION* (wildcard)
        permissions = [
            x["SK"]["S"].removeprefix("PERMISSION#")
            for x in result["Items"]
            if x["PK"]["S"] == pk_key_item
            and x["SK"]["S"] == f"PERMISSION#{method_resource}"
        ]

        return len(permissions) > 0
