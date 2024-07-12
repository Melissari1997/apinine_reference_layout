from typing import List, Tuple
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
    tiff_metadata: List[str],
    coordinates: List[Tuple[str, str, str]],
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

    tiff_metadata: List[str]
        List of metadata associated with the file

    coordinates : List[Tuple[str, str, str]]
        List of coordinates to be processed. Every coordinate is defined by: (lat, lon, address).

    geocoder : Geocoder
        Object use for the geocoding. If address is supplied, it must not be None.
    geodatareader : GeoDataReader
        Object use for reading the data.

    Returns
    -------
    dict
        Dictionary containing info about the location and the flood risk assessment.
    """

    # https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/geocoding.py.
    # There isn't a method for batch geocoding

    points: List[Tuple[str, str]] = []  # [(lat, lon), (lat, lon)]
    for lat, lon, address in coordinates:
        if lat is not None and lon is not None:
            points.append((lat, lon))
        else:
            calculated_lat, calculated_lon = geocoder.geocode(address)
            points.append((calculated_lat, calculated_lon))

    values = geodatareader.sample_data_points(
        filename=filename,
        coordinates=points,
        metadata=tiff_metadata,
    )

    return values
