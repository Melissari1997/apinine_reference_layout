from aws_lambda_powertools import Logger, Tracer
from common.event_parser import parse_aws_event
from common.response import handle_response
from common.schema import NOT_IMPLEMENTED_PLACEHOLDER
from geocoder.geocoder import Geocoder
from geocoder.gmaps_geocoder import GMapsGeocoder
from readgeodata.interfaces import GeoDataReader
from readgeodata.rasterioreader import RasterIOReader
from schema import OutputSchema

logger = Logger()
tracer = Tracer()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


class DroughtKeys:
    """Name of the band names to read from the geotiff."""

    DURATION_RP20 = "duration_rp20y"
    DURATION_RP100 = "duration_rp100y"
    DURATION_RP200 = "duration_rp200y"
    SEVERITY_RP20 = "severity_rp20y"
    SEVERITY_RP100 = "severity_rp100y"
    SEVERITY_RP200 = "severity_rp200y"


@tracer.capture_method
def main(
    filename: str,
    address: str,
    lon: float,
    lat: float,
    geocoder: Geocoder,
    geodatareader: GeoDataReader,
) -> dict:
    """Compute the drought risk assessment for a location.

    The data is retrieved from a file (usually a .tif file) by the
    geodatareader,which samples the file in the specified set of
    coordinates (lat, lon).

    If an address is provided instead, retrieve the corresponding
    coordinates first using the geocoder object.

    Parameters
    ----------
    filename : str
        Path of the file to read data from.
    address : str
        Address to query.
    lon : float
        Longitude to query. If supplied, the 'lat' param must be supplied as well.
    lat : float
        Latitude to query. If supplied, the 'lat' param must be supplied as well.
    geocoder : Geocoder
        Object use for the geocoding. If address is supplied, it must not be None.
    geodatareader : GeoDataReader
        Object use for reading the data.

    Returns
    -------
    dict
        Dictionary containing info about the location and the drought risk assessment.
    """
    if address:
        logger.info(f"Geocoding address: '{address}'")
        (lon, lat), address = geocoder.geocode(address)

    logger.info(
        f"Starting drought risk assessment with filename: '{filename}', address: '{address}', lat: '{lat}', lon: '{lon}'"
    )
    values = geodatareader.sample_data_points(
        filename=filename, coordinates=[(lon, lat)]
    )

    output = {
        "address": address,
        "lat": lat,
        "lon": lon,
        "drought_risk_assessment": {
            "return_period_20y": {
                "intensity": {
                    "duration_months": values[DroughtKeys.DURATION_RP20][0],
                    "severity": values[DroughtKeys.SEVERITY_RP20][0],
                },
                "vulnerability": NOT_IMPLEMENTED_PLACEHOLDER,
            },
            "return_period_100y": {
                "intensity": {
                    "duration_months": values[DroughtKeys.DURATION_RP100][0],
                    "severity": values[DroughtKeys.SEVERITY_RP100][0],
                },
                "vulnerability": NOT_IMPLEMENTED_PLACEHOLDER,
            },
            "return_period_200y": {
                "intensity": {
                    "duration_months": values[DroughtKeys.DURATION_RP200][0],
                    "severity": values[DroughtKeys.SEVERITY_RP200][0],
                },
                "vulnerability": NOT_IMPLEMENTED_PLACEHOLDER,
            },
        },
        "risk_index": NOT_IMPLEMENTED_PLACEHOLDER,
        "average_annual_loss": {
            "value": NOT_IMPLEMENTED_PLACEHOLDER,
            "national_average": NOT_IMPLEMENTED_PLACEHOLDER,
            "regional_average": NOT_IMPLEMENTED_PLACEHOLDER,
        },
        "hazard_index": NOT_IMPLEMENTED_PLACEHOLDER,
    }

    return output


@handle_response(validate_schema=OutputSchema)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: dict = None) -> dict:
    filename, address, lat, lon = parse_aws_event(event)

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
