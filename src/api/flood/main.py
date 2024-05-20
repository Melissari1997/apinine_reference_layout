from aws_lambda_powertools import Logger, Tracer
from common.schema import NOT_IMPLEMENTED_PLACEHOLDER
from geocoder.geocoder import Geocoder
from geocoder.gmaps_geocoder import GMapsGeocoder
from land_use.util_CLC_conversion import CLC_MAPPING
from readgeodata.interfaces import GeoDataReader
from readgeodata.rasterioreader import RasterIOReader

logger = Logger()
tracer = Tracer()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


class FloodKeys:
    """Name of the fields to read from the geotiff.
    These are all band names except 'NATIONAL_AAL'
    which is a metadata field.
    """

    LAND_USE = "land_use"
    WH_20 = "water_intensity_rp20"
    WH_100 = "water_intensity_rp100"
    WH_200 = "water_intensity_rp200"
    VULN_20 = "vulnerability_rp20"
    VULN_100 = "vulnerability_rp100"
    VULN_200 = "vulnerability_rp200"
    AAL = "aal"
    RISK_INDEX = "risk_index"

    NATIONAL_AAL = "STATISTICS_MEAN"
    AGRICULTURE_AAL = "Average_Agriculture_AAL"
    COMMERCIAL_AAL = "Average_Commercial_AAL"
    INDUSTRIAL_AAL = "Average_Industrial_AAL"
    INFRASTRUCTURE_AAL = "Average_Infrastructure_AAL"
    RESIDENTIAL_AAL = "Average_Residential_AAL"
    NONE_AAL = "Average_None_AAL"


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
        filename=filename,
        coordinates=[(lon, lat)],
        metadata=[
            FloodKeys.AGRICULTURE_AAL,
            FloodKeys.COMMERCIAL_AAL,
            FloodKeys.INDUSTRIAL_AAL,
            FloodKeys.INFRASTRUCTURE_AAL,
            FloodKeys.RESIDENTIAL_AAL,
            FloodKeys.NONE_AAL,
        ],
    )
    land_use = CLC_MAPPING[values[FloodKeys.LAND_USE][0]]

    output = {
        "address": address,
        "lat": lat,
        "lon": lon,
        "land_use": land_use,
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
        "average_annual_loss": {
            "value": values[FloodKeys.AAL][0],
            "national_average": values["metadata"][f"Average_{land_use}_AAL"],
            "regional_average": NOT_IMPLEMENTED_PLACEHOLDER,
        },
        "risk_index": values[FloodKeys.RISK_INDEX][0],
        "hazard_index": NOT_IMPLEMENTED_PLACEHOLDER,
    }

    return output
