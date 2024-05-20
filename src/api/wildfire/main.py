from aws_lambda_powertools import Logger, Tracer
from common.schema import NOT_IMPLEMENTED_PLACEHOLDER
from geocoder.geocoder import Geocoder
from geocoder.gmaps_geocoder import GMapsGeocoder
from readgeodata.interfaces import GeoDataReader
from readgeodata.rasterioreader import RasterIOReader

logger = Logger()
tracer = Tracer()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


class WildfireKeys:
    """Name of the band names to read from the geotiff."""

    FWI_2 = "wildfire rp 2 layer, band 1"
    FWI_10 = "wildfire rp 10 layer, band 2"
    FWI_30 = "wildfire rp 30 layer, band 3"


@tracer.capture_method
def main(
    filename: str,
    address: str,
    lon: float,
    lat: float,
    geocoder: Geocoder,
    geodatareader: GeoDataReader,
) -> dict:
    """Compute the wildfire risk assessment for a location.

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
        Dictionary containing info about the location and the wildfire risk assessment.
    """
    if address:
        logger.info(f"Geocoding address: '{address}'")
        (lon, lat), address = geocoder.geocode(address)

    logger.info(
        f"Starting wildfire risk assessment with filename: '{filename}', address: '{address}', lat: '{lat}', lon: '{lon}'"
    )
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
                "vulnerability": NOT_IMPLEMENTED_PLACEHOLDER,
            },
            "return_period_10y": {
                "intensity": {
                    "fwi": values[WildfireKeys.FWI_10][0],
                },
                "vulnerability": NOT_IMPLEMENTED_PLACEHOLDER,
            },
            "return_period_30y": {
                "intensity": {
                    "fwi": values[WildfireKeys.FWI_30][0],
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
