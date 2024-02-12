import json
import os

import boto3
import googlemaps
from botocore.exceptions import ClientError

from geocoder.geocoder import (
    FailedGeocodeError,
    Geocoder,
    MultipleMatchesForAddressError,
    OutOfBoundsError,
)


class GMapsGeocoder(Geocoder):
    def __init__(self) -> None:
        self.gmaps_client = None

    def _setup_client(self):
        self.gmaps_client = googlemaps.Client(
            key=self._get_api_secret_key_from_aws()["gmaps_api_key"]
        )

    def _get_api_secret_key_from_aws(self):
        # If you need more information about configurations
        # or implementing the sample code, visit the AWS docs:
        # https://aws.amazon.com/developer/language/python/

        secret_name = os.environ.get("GMAPS_SECRET_NAME")
        region_name = os.environ.get("GMAPS_SECRET_REGION", "eu-central-1")

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response["SecretString"]

        # Your code goes here.
        return json.loads(secret)

    def _valid_location(self, geocode_result: str) -> bool:
        valid_countries = ["Italy"]
        country = next(
            filter(
                lambda comp: "country" in comp["types"],
                geocode_result["address_components"],
            )
        )["long_name"]
        return country in valid_countries

    def geocode(self, address: str) -> tuple[tuple[float, float], str]:
        # Lazy init
        if not self.gmaps_client:
            self._setup_client()

        geocode_result = self.gmaps_client.geocode(address)
        result_size = len(geocode_result)

        if result_size == 0:
            raise FailedGeocodeError("Unable to resolve address " + address)
        if result_size > 1:
            raise MultipleMatchesForAddressError

        geocode_result = geocode_result[0]
        if not self._valid_location(geocode_result):
            raise OutOfBoundsError

        coords, formatted_address = (
            (
                geocode_result["geometry"]["location"]["lng"],
                geocode_result["geometry"]["location"]["lat"],
            ),
            geocode_result["formatted_address"],
        )
        return coords, formatted_address
