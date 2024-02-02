import abc

import argon2


class Key:
    def __init__(self):
        self.password_hasher = argon2.PasswordHasher(
            time_cost=1, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16
        )

    def save_key_and_permission(
        self, api_key_gen, repository, name, description, permissions, organization
    ):
        value = api_key_gen.create_api_key(name, description)

        print(f"vlaue: {value}")
        # Hash the value
        user, secret = value.split(":")
        hashed_key = self.password_hasher.hash(secret)
        print(f"Hashed key: {hashed_key}")
        repository.save_key_and_permission(hashed_key, permissions, organization, user)
        print("Saved item")


# Domain interface
class KeyGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_api_key(self, name, description):
        raise NotImplementedError


class KeyRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save_key_and_permission(self, hashed_key, permissions, organization, user):
        raise NotImplementedError
