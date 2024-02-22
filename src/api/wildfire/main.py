import os

from aws_lambda_powertools import Logger
from common.input_schema import querystring_schema
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


class WildfireKeys:
    FWI_2 = "wildfire rp 2 layer, band 1"
    FWI_10 = "wildfire rp 10 layer, band 2"
    FWI_30 = "wildfire rp 30 layer, band 3"


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
        filename=filename, coordinates=[(lon, lat)]
    )

    output = {
        "address": address,
        "lat": lat,
        "lon": lon,
        "wildfire_risk_assessment": {
            "return_period_2y": {
                "intensity": {
                    "fwi": values[WildfireKeys.FWI_2][0],
                },
                "vulnerability": "Not implemented",
            },
            "return_period_10y": {
                "intensity": {
                    "fwi": values[WildfireKeys.FWI_10][0],
                },
                "vulnerability": "Not implemented",
            },
            "return_period_30y": {
                "intensity": {
                    "fwi": values[WildfireKeys.FWI_30][0],
                },
                "vulnerability": "Not implemented",
            },
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
