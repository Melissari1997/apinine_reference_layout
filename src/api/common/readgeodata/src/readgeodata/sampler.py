from typing import List, Tuple
from aws_lambda_powertools import Logger, Tracer
from geocoder.geocoder import Geocoder
from geocoder.gmaps_geocoder import GMapsGeocoder
from readgeodata.interfaces import GeoDataReader
from readgeodata.rasterioreader import RasterIOReader
from typing import Dict
import numpy as np


logger = Logger()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


def convert_ndarrays_to_lists(data_dict: Dict) -> Dict:
    """Convert ndarray values in the dictionary to lists."""
    for key in data_dict:
        if isinstance(data_dict[key], np.ndarray):
            data_dict[key] = data_dict[key].tolist()
    return data_dict


def split_coordinates(
    coordinates: List[Tuple[float, float, str]]
) -> Tuple[List[float], List[float], List[str]]:
    """
    Split list of coordinates into separate lists for latitudes, longitudes, and addresses.

    Args:
        coordinates (List[Tuple[float, float, str]]): List of tuples containing latitude, longitude, and address.

    Returns:
        Tuple[List[float], List[float], List[str]]: Separate lists for latitudes, longitudes, and addresses.
    """
    points_array = np.array(coordinates)
    latitudes = points_array[:, 0].tolist()
    longitudes = points_array[:, 1].tolist()
    addresses = points_array[:, 2].tolist()
    return latitudes, longitudes, addresses


def sample(
    filename: str,
    tiff_metadata: List[str],
    coordinates: List[Tuple[str, str, str]],
    geocoder: Geocoder,
    geodatareader: GeoDataReader,
) -> dict:
    """
    Sample data from a file

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
        Metadatas to fetch from file, by default None.

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

    converted_values = convert_ndarrays_to_lists(values)
    latitudes, longitudes, addresses = split_coordinates(coordinates)
    converted_values.update(
        {"latitude": latitudes, "longitude": longitudes, "addresses": addresses}
    )

    return values
