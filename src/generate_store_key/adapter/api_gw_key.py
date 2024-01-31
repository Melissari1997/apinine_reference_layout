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

    def create_api_key(self, name, description):
        response = self.apigw_client.create_api_key(
            name=name,
            description=description,
            enabled=True,
            value=self._buid_api_key(),
        )

        value = response["value"]

        return value

    def _buid_api_key(self):
        user = "".join(
            [secrets.choice(self.key_alphabet) for i in range(self.user_length)]
        )
        secret = "".join(
            [secrets.choice(self.key_alphabet) for i in range(self.secret_length)]
        )

        key = f"{user}:{secret}"

        return key
