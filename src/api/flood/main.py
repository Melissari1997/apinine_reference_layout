from common.errors import ConflictingInputsError
from common.geocoder.gmaps_geocoder import GMapsGeocoder
from common.readgeodata.rasterioreader import RasterIOReader
from common.response import handle_response


class FloodKeys:
    WH_20 = "20 layer, band 1"
    WH_100 = "100 layer, band 2"
    WH_200 = "200 layer, band 3"
    VULN_20 = "vuln_20 layer, band 4"
    VULN_100 = "vuln_100 layer, band 5"
    VULN_200 = "vuln_200 layer, band 6"
    AAL = "aal layer, band 7"
    RISK_INDEX = "risk_ind layer, band 8"


def main(address: str = None, lon: float = None, lat: float = None) -> dict:
    correct = (address and not (lon or lat)) or ((lon and lat) and not address)
    if not correct:
        raise ConflictingInputsError

    if address:
        (lon, lat), address = GMapsGeocoder().geocode(address)

    filename = "s3://mlflow-monitoring/93/cf7509a33fe543a9a87aa7658e551659/artifacts/inference/aal_baseline_8bands.tif"
    reader = RasterIOReader()
    values = reader.sample_data_points(filename=filename, coordinates=[(lon, lat)])

    output = {
        "address": address,
        "flood_risk_assessment": {
            "return_period_20y": {
                "intensity": {"water_height": values[FloodKeys.WH_20][0]},
                "vulnerability": values[FloodKeys.VULN_20][0],
            },
            "return_period_100y": {
                "intensity": {"water_height": values[FloodKeys.WH_100][0]},
                "vulnerability": values[FloodKeys.VULN_100][0],
            },
            "return_period_200y": {
                "intensity": {"water_height": values[FloodKeys.WH_200][0]},
                "vulnerability": values[FloodKeys.VULN_200][0],
            },
        },
        "risk_index": values[FloodKeys.RISK_INDEX][0],
        "average_annual_loss": values[FloodKeys.AAL][0],
        "national_average_annual_loss": 0.0423,
    }

    return output


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
