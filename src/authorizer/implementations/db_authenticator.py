from datetime import datetime

import argon2
from interfaces import Authenticator, KeyDB


class DBAuthenticator(Authenticator):
    def __init__(self, key_db: KeyDB) -> None:
        self.password_hasher = argon2.PasswordHasher(
            time_cost=1, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16
        )
        self.key_db = key_db

    def authorize(self, key):
        hashed_key = self.password_hasher.hash(key)
        pk_key_item = f"KEY#{hashed_key}"
        result = self.key_db.query_by_key(pk_key_item)  # noqa: F841

        if result["Count"] == 0:
            raise Exception("Unauthorized")  # Return immediately

        now_ts = datetime.now().timestamp()
        # Get the key item (PK and SK === KEY#....)
        key_item = [
            x
            for x in result["Items"]
            if x["PK"] == pk_key_item and x["SK"] == pk_key_item
        ][0]
        if int(key_item["expires_at"]) < now_ts:
            raise Exception("Unauthorized")  # Return immediately

        self.key_db.update_last_accessed(last_accessed_ts=now_ts)
        # TODO: extract permissions from result

        permissions = []

        return permissions
