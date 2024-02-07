from api.common.errors.errors import ConflictingInputsError
from api.common.errors.handler import exception_handler
from api.common.implementations.gmaps_geocoder import GMapsGeocoder


def main(address: str, lat: float, lon: float) -> dict:
    if lat and lon and address:
        raise ConflictingInputsError(
            "Either 'address' or 'lat' and 'long' parameters must be supplied - not both."
        )
    if address:
        (lat, lon), address = GMapsGeocoder().geocode(address)

    output_placeholder = {
        "address": "Via Milazzo, 193, 27100 Pavia PV, Italy",
        "flood_risk_assessment": {
            "return_period_20y": {
                "intensity": {"water_height": 2.6},
                "vulnerability": 0.81,
            },
            "return_period_100y": {
                "intensity": {"water_height": 2.7},
                "vulnerability": 0.82,
            },
            "return_period_200y": {
                "intensity": {"water_height": 2.7},
                "vulnerability": 0.82,
            },
        },
        "risk_index": 5,
        "average_annual_loss": 0.0408,
    }

    return output_placeholder


@exception_handler
def handler(event, context=None):
    query_params = event["queryStringParameters"]
    address = query_params.get("address")
    lat = query_params.get("lat")
    lon = query_params.get("lon")
    return main(address=address, lat=lat, lon=lon)


if __name__ == "__main__":
    event = {"queryStringParameters": {"address": "via verruca 1 trento"}}

    result = handler(event)
    print(result, type(result))
