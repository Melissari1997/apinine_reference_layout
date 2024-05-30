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


class WildfireKeys:
    """Name of the band names to read from the geotiff."""

    FWI_2 = "intensity_rp2"
    FWI_10 = "intensity_rp10"
    FWI_30 = "intensity_rp30"
    VULN_2 = "vulnerability_rp2"
    VULN_10 = "vulnerability_rp10"
    VULN_30 = "vulnerability_rp30"
    AAL = "aal"
    LAND_USE = "land_use"
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
        filename=filename,
        coordinates=[(lon, lat)],
        metadata=[
            WildfireKeys.AGRICULTURE_AAL,
            WildfireKeys.COMMERCIAL_AAL,
            WildfireKeys.INDUSTRIAL_AAL,
            WildfireKeys.INFRASTRUCTURE_AAL,
            WildfireKeys.RESIDENTIAL_AAL,
            WildfireKeys.NONE_AAL,
        ],
    )

    land_use = CLC_MAPPING[values[WildfireKeys.LAND_USE][0]]

    output = {
        "address": address,
        "lat": lat,
        "lon": lon,
        "land_use": land_use,
        "wildfire_risk_assessment": {
            "return_period_2y": {
                "intensity": {
                    "fwi": values[WildfireKeys.FWI_2][0],
                },
                "vulnerability": values[WildfireKeys.VULN_2][0],
            },
            "return_period_10y": {
                "intensity": {
                    "fwi": values[WildfireKeys.FWI_10][0],
                },
                "vulnerability": values[WildfireKeys.VULN_10][0],
            },
            "return_period_30y": {
                "intensity": {
                    "fwi": values[WildfireKeys.FWI_30][0],
                },
                "vulnerability": values[WildfireKeys.VULN_30][0],
            },
        },
        "risk_index": values[WildfireKeys.RISK_INDEX][0],
        "average_annual_loss": {
            "value": values[WildfireKeys.AAL][0],
            "national_average": values["metadata"][f"Average_{land_use}_AAL"],
            "regional_average": NOT_IMPLEMENTED_PLACEHOLDER,
        },
        "hazard_index": NOT_IMPLEMENTED_PLACEHOLDER,
    }

    return output
