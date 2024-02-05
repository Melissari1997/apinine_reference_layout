import abc
import json

import argon2
import boto3


class Key:
    def __init__(self):
        # Read configurations from SSM Parameter store
        client = boto3.client("ssm")
        response = client.get_parameter(Name="authorizer_hasher_config")
        hasher_config = json.loads(response["Parameter"]["Value"])
        time_cost = hasher_config["time_cost"]
        memory_cost = hasher_config["memory_cost"]
        parallelism = hasher_config["parallelism"]
        hash_len = hasher_config["hash_len"]
        salt_len = hasher_config["salt_len"]

        self.password_hasher = argon2.PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=hash_len,
            salt_len=salt_len,
        )
        print(f"Hasher config {hasher_config}, {self.password_hasher._parameters}")

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
