from typing import List, Tuple
from aws_lambda_powertools import Logger
from geocoder.geocoder import (
    FailedGeocodeError,
    Geocoder,
    MultipleMatchesForAddressError,
    OutOfBoundsError,
)
from geocoder.gmaps_geocoder import GMapsGeocoder
from readgeodata.interfaces import GeoDataReader
from readgeodata.rasterioreader import RasterIOReader
from typing import Dict
import numpy as np


logger = Logger()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


def extend_lists_in_dict(input_dict, M, fill_value=None, exclude_keys=["metadata"]):
    return {
        k: (v + [fill_value] * (M - len(v)) if k not in exclude_keys else v)
        for k, v in input_dict.items()
    }


def convert_ndarrays_to_lists(data_dict: Dict) -> Dict:
    """
    Convert ndarray values in the dictionary to lists.

    Args:
        data_dict (Dict): Input dictionary possibly containing ndarray values.

    Returns:
        Dict: Dictionary with ndarray values converted to lists.
    """
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
    coordinates: List[Tuple[str, str, str]],
    geodatareader: GeoDataReader,
    tiff_tags: List[str] = None,
) -> dict:
    """
    Sample data from a file based on given coordinates or addresses.

    Retrieves data from a specified file using a geodatareader,
    sampling the file at coordinates (lat, lon). If addresses are provided,
    it first retrieves corresponding coordinates using the geocoder object.

    Args:
        filename (str): Path of the file to read data from.
        tiff_tags (List[str]): Metadata to fetch from the file.
        coordinates (List[Tuple[str, str, str]]): List of coordinates or addresses to process.
            Each tuple is (lon, lat, address).
        geocoder (Geocoder): Object for geocoding addresses to coordinates.
        geodatareader (GeoDataReader): Object for reading geo data from file.

    Returns:
        dict: Dictionary containing sampled data and location information.
    """
    if tiff_tags is None:
        tiff_tags = []

    print(f"Processing coords: {coordinates}")

    values = geodatareader.sample_data_points(
        filename=filename,
        coordinates=[(lon, lat) for lat, lon, _ in coordinates],
        metadata=tiff_tags,
    )

    converted_values = convert_ndarrays_to_lists(values)

    return converted_values
