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
        result = self.key_db.query_by_key(hashed_key)  # noqa: F841
        # TODO: check non empty result

        now_ts = datetime.now().timestamp()
        # TODO: check expiration time

        self.key_db.update_last_accessed(last_accessed_ts=now_ts)
        # TODO: extract permissions from result

        permissions = []

        return permissions
