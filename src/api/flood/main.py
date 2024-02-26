from aws_lambda_powertools import Logger, Tracer
from common.event_parser import parse_aws_event
from common.response import handle_response
from geocoder.geocoder import Geocoder
from geocoder.gmaps_geocoder import GMapsGeocoder
from readgeodata.interfaces import GeoDataReader
from readgeodata.rasterioreader import RasterIOReader
from schema import OutputSchema

logger = Logger()
tracer = Tracer()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


class FloodKeys:
    """Name of the fields to read from the geotiff.
    These are all band names except 'NATIONAL_AAL'
    which is a metadata field.
    """

    WH_20 = "20 layer, band 1"
    WH_100 = "100 layer, band 2"
    WH_200 = "200 layer, band 3"
    VULN_20 = "vuln_20 layer, band 4"
    VULN_100 = "vuln_100 layer, band 5"
    VULN_200 = "vuln_200 layer, band 6"
    AAL = "aal layer, band 7"
    RISK_INDEX = "risk_ind layer, band 8"
    NATIONAL_AAL = "STATISTICS_MEAN"


@tracer.capture_method
def main(
    filename: str,
    address: str,
    lon: float,
    lat: float,
    geocoder: Geocoder,
    geodatareader: GeoDataReader,
) -> dict:
    """Compute the flood risk assessment for a location.

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
        Dictionary containing info about the location and the flood risk assessment.
    """
    if address:
        logger.info(f"Geocoding address: '{address}'")
        (lon, lat), address = geocoder.geocode(address)

    logger.info(
        f"Starting flood risk assessment with filename: '{filename}', address: '{address}', lat: '{lat}', lon: '{lon}'"
    )
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
