import googlemaps

from ..utils.aws import get_api_secret_key_from_aws
from .geocoder import FailedGeocodeError, Geocoder


class GMapsGeocoder(Geocoder):
    def __init__(self) -> None:
        self.gmaps_client = googlemaps.Client(
            key=get_api_secret_key_from_aws()["gmaps_api_key"]
        )

    def geocode(self, address: str) -> tuple[tuple[float, float], str]:
        geocode_result = self.gmaps_client.geocode(address)
        try:
            coords, formatted_address = (
                (
                    geocode_result[0]["geometry"]["location"]["lng"],
                    geocode_result[0]["geometry"]["location"]["lat"],
                ),
                geocode_result[0]["formatted_address"],
            )
            return coords, formatted_address
        except Exception as exc:
            raise FailedGeocodeError("Unable to resolve address " + address) from exc
