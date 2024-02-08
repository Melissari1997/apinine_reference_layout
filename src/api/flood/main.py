from common.errors import ConflictingInputsError
from common.geocoder.gmaps_geocoder import GMapsGeocoder
from common.response import handle_response


def main(address: str = None, lon: float = None, lat: float = None) -> dict:
    correct = (address and not (lon or lat)) or ((lon and lat) and not address)
    if not correct:
        raise ConflictingInputsError

    if address:
        (lon, lat), address = GMapsGeocoder().geocode(address)

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


@handle_response
def handler(event, context=None):
    query_params = event["queryStringParameters"]
    address = query_params.get("address")
    lat = query_params.get("lat")
    lon = query_params.get("lon")
    return main(address=address, lat=lat, lon=lon)


# if __name__ == "__main__":
#     event = {"queryStringParameters": {"address": "via verruca 1 trento"}}

#     result = handler(event)
#     print(result, type(result))
