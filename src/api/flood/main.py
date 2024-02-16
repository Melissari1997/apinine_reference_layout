import os

from aws_lambda_powertools import Logger
from common.response import handle_response
from geocoder.geocoder import Geocoder
from geocoder.gmaps_geocoder import GMapsGeocoder
from jsonschema import validate
from readgeodata.interfaces import GeoDataReader
from readgeodata.rasterioreader import RasterIOReader
from schema import OutputSchema

logger = Logger()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()

# Allow only lat-lon or address
querystring_schema = {
    "type": "object",
    "oneOf": [{"required": ["lat", "lon"]}, {"required": ["address"]}],
    "properties": {
        "lat": {"type": "number", "minimum": 27, "maximum": 72},
        "lon": {"type": "number", "minimum": -22, "maximum": 45},
        "address": {"type": "string", "minLength": 1},
    },
}


class FloodKeys:
    WH_20 = "20 layer, band 1"
    WH_100 = "100 layer, band 2"
    WH_200 = "200 layer, band 3"
    VULN_20 = "vuln_20 layer, band 4"
    VULN_100 = "vuln_100 layer, band 5"
    VULN_200 = "vuln_200 layer, band 6"
    AAL = "aal layer, band 7"
    RISK_INDEX = "risk_ind layer, band 8"
    NATIONAL_AAL = "STATISTICS_MEAN"


def main(
    filename: str,
    address: str,
    lon: float,
    lat: float,
    geocoder: Geocoder,
    geodatareader: GeoDataReader,
) -> dict:
    if address:
        (lon, lat), address = geocoder.geocode(address)

    logger.info(f"MAIN: {filename}")
    values = geodatareader.sample_data_points(
        filename=filename, coordinates=[(lon, lat)], metadata=["STATISTICS_MEAN"]
    )

    output = {
        "address": address,
        "lat": lat,
        "lon": lon,
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
        "average_annual_loss": {
            "value": values[FloodKeys.AAL][0],
            "national_average": values["metadata"][FloodKeys.NATIONAL_AAL],
        },
    }

    return output


@handle_response(validate_schema=OutputSchema)
@logger.inject_lambda_context
def handler(event, context=None):
    filename = os.environ.get("GEOTIFF_PATH")

    if filename is None:
        raise ValueError("Missing env var GEOTIFF_PATH")

    query_params = event.get("queryStringParameters", None)

    validate(instance=query_params, schema=querystring_schema)

    address = query_params.get("address")

    lat = query_params.get("lat")
    if lat is not None:
        lat = float(lat)

    lon = query_params.get("lon")
    if lon is not None:
        lon = float(lon)

    response = main(
        filename=filename,
        address=address,
        lat=lat,
        lon=lon,
        geocoder=gmapsgeocoder,
        geodatareader=riogeoreader,
    )

    logger.info(f"Returning response: {response}")
    return response
