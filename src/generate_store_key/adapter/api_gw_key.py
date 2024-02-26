import secrets
import string

import boto3
from domain.key import KeyGenerator


class ApiGwKeyGenerator(KeyGenerator):
    def __init__(
        self,
    ) -> None:
        self.apigw_client = boto3.client("apigateway")
        self.key_alphabet = string.ascii_letters + string.digits
        self.user_length = 16
        self.secret_length = 32

    def create_api_key(self, name: str, description: str) -> str:
        """Generate an API key.

        This is just a wrapper around the self.apigw_client.create_api_key() method.

        Parameters
        ----------
        name : str
            Key name.
        description : str
            Key description.

        Returns
        -------
        key: str
            Generated key.
        """
        response = self.apigw_client.create_api_key(
            name=name,
            description=description,
            enabled=True,
            value=self._build_api_key(),
        )

        value = response["value"]

        return value

    def _build_api_key(self):
        """Generate a custom API key.

        The key is made of two logical parts: the 'user' part and the 'secret' part.
        Both are randomly-generated strings. The 'user' part will be stored in the db as
        it is. The 'secret' part will be hashed first with a criptographically-secure
        function.

        Returns
        -------
        key: str
            API key as user:secret.
        """
        user = "".join(
            [secrets.choice(self.key_alphabet) for i in range(self.user_length)]
        )
        secret = "".join(
            [secrets.choice(self.key_alphabet) for i in range(self.secret_length)]
        )

        key = f"{user}:{secret}"

        return key
