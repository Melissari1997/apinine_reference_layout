import os
from datetime import datetime

import argon2
from aws_lambda_powertools import Logger
from interfaces import Authenticator, KeyDB

logger = Logger()


class DBAuthenticator(Authenticator):
    def __init__(self, key_db: KeyDB) -> None:
        """Constructor for DBAuthenticator.

        Create the Argon2 password hasher from the required env variables.

        Args:
            key_db (KeyDB): Database used to retrieve the permissions from the API key.
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

    def authorize(self, key: str, method: str, resource: str) -> bool:
        """Authorize an API operation.

        Check whether the provided key has is allowed to perform
        the provided method on the provided resource.

        Parameters
        ----------
        key : str
            API key in the form myuser:mysecret
        method : str
            HTTP method of the request (e.g. GET).
        resource : str
            Endpoint of the requested resource (e.g. /flood/rcp85).

        Returns
        -------
        bool
            True if the operation is allowed, False otherwise.

        Raises
        ------
        ValueError
            Invalid key format.
        ValueError
            The hash or the hasher have been changed.
        ValueError
            The sort key was not found. Data may be inconsistent.
            This is probably the result of someone messing with keys manually.
        ValueError
            Key is expired.
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
