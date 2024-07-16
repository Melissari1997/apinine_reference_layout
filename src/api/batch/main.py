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
        List of coordinates to be processed. Every coordinate is defined by: (lon, lat, address).

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

    points: List[Tuple[str, str]] = []  # [(lat, lat), (lat, lon)]
    for lat, lon, address in coordinates:
        if lat is not None and lon is not None:
            points.append((lon, lat))
        else:
            calculated_lat, calculated_lon = geocoder.geocode(address)
            points.append((calculated_lon, calculated_lat))

    print(f"Sample points: {points}")

    # TODO handle different crs
    values = geodatareader.sample_data_points(
        filename=filename,
        coordinates=points,
        metadata=tiff_metadata,
    )

    return values
