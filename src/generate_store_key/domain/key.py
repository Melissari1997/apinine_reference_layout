import abc
import json

import argon2
import boto3


# Domain interface
class KeyGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_api_key(self, name: str, description: str):  # noqa: ANN201
        raise NotImplementedError


class KeyRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save_key_and_permission(  # noqa: ANN201
        self, hashed_key: str, permissions: list[str], organization: str, user: str
    ):
        raise NotImplementedError


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
        self,
        api_key_gen: KeyGenerator,
        repository: KeyRepository,
        name: str,
        description: str,
        permissions: list[str],
        organization: str,
    ) -> None:
        """Generate a new API key and store it in the repository.

        So far, the key is generated through Amazon API Gateway and stored on a DynamoDB table.

        Parameters
        ----------
        api_key_gen : KeyGenerator
            Object used to generate the API key.
        repository : KeyRepository
            Object used to store the API key on a backend.
        name : str
            Name of the key to be generated.
        description : str
            Description of the key to be generated.
        permissions : list[str]
            List of resources the generated key will be allowed to access.
        organization : str
            Organization of the key to be generated.
        """
        value = api_key_gen.create_api_key(name, description)

        print(f"value: {value}")
        # Hash the value
        user, secret = value.split(":")
        hashed_key = self.password_hasher.hash(secret)
        print(f"Hashed key: {hashed_key}")
        repository.save_key_and_permission(
            hashed_key=hashed_key,
            permissions=permissions,
            organization=organization,
            user=user,
        )
        print("Saved item")
