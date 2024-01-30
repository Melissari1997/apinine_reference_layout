import boto3
from domain.key import KeyGenerator


class ApiGwKeyGenerator(KeyGenerator):
    def __init__(
        self,
    ) -> None:
        self.apigw_client = boto3.client("apigateway")

    def create_api_key(self, name, description):
        response = self.apigw_client.create_api_key(
            name=name,
            description=description,
            enabled=True,
        )

        value = response["value"]

        return value
