from io import StringIO
from typing import Any, List, NamedTuple, Tuple, Dict

from aws_lambda_powertools import Logger, Tracer
from land_use.util_CLC_conversion import CLC_MAPPING, DamageCurveEnum
from readgeodata.sampler import sample
from geocoder.geocoder import (
    FailedGeocodeError,
    MultipleMatchesForAddressError,
    OutOfBoundsError,
)
from common.event_parser import (
    get_bucket_and_key,
    parse_s3_file_upload_event,
)
from geocoder.gmaps_geocoder import GMapsGeocoder
from readgeodata.rasterioreader import RasterIOReader
import csv
import boto3
import io
import numpy as np

# Initialize Logger, Tracer, Geocoder, and GeoReader
logger = Logger()
tracer = Tracer()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


class GeocodedPoint(NamedTuple):
    lat: float
    lon: float
    recognized_lat: float
    recognized_lon: float
    address: str
    recognized_address: str
    message: str


class TiffTagsKeys:
    """Name of the  metadata fields to read from the geotiff."""

    NATIONAL_AAL = "STATISTICS_MEAN"
    AGRICULTURE_AAL = "Average_Agriculture_AAL"
    COMMERCIAL_AAL = "Average_Commercial_AAL"
    INDUSTRIAL_AAL = "Average_Industrial_AAL"
    INFRASTRUCTURE_AAL = "Average_Infrastructure_AAL"
    RESIDENTIAL_AAL = "Average_Residential_AAL"
    NONE_AAL = "Average_None_AAL"


def separate_valid_points(
    coordinates: List[Tuple[str, str, str]], geocoder
) -> Tuple[List[GeocodedPoint], List[GeocodedPoint]]:
    """
    Separate valid and invalid points based on provided coordinates or addresses.

    Uses a geocoder to convert addresses into coordinates where necessary,
    and separates valid points from invalid points.

    Args:
        coordinates (List[Tuple[str, str, str]]): List of coordinates or addresses to process.
            Each tuple is (lon, lat, address).
        geocoder: Object for geocoding addresses to coordinates.

    Returns:
        Tuple[List[GeocodedPoint], List[GeocodedPoint]]: Two lists of GeocodedPoint objects,
        the first containing valid points and the second containing invalid points.
    """
    valid_points = []
    not_valid_points = []

    for lat, lon, address in coordinates:
        if lat is not None and lon is not None:
            valid_points.append(
                GeocodedPoint(
                    lon=lon,
                    lat=lat,
                    recognized_lon=None,
                    recognized_lat=None,
                    address=address,
                    recognized_address=None,
                    message=None,
                )
            )
        else:
            try:
                calculated_coords, calculated_address = geocoder.geocode(address)
                calculated_lon, calculated_lat = calculated_coords
                valid_points.append(
                    GeocodedPoint(
                        lon=None,
                        lat=None,
                        recognized_lon=calculated_lon,
                        recognized_lat=calculated_lat,
                        address=address,
                        recognized_address=calculated_address,
                        message=None,
                    )
                )
            except FailedGeocodeError as failed_geocode:
                logger.error(failed_geocode.__traceback__)
                not_valid_points.append(
                    GeocodedPoint(
                        lon=None,
                        lat=None,
                        recognized_lon=None,
                        recognized_lat=None,
                        address=address,
                        recognized_address=None,
                        message="Failed Geocoding",
                    )
                )
            except MultipleMatchesForAddressError as multiple_match_geocode:
                logger.error(multiple_match_geocode.__traceback__)
                not_valid_points.append(
                    GeocodedPoint(
                        lon=None,
                        lat=None,
                        recognized_lon=None,
                        recognized_lat=None,
                        address=address,
                        recognized_address=None,
                        message="Multiple Matches For Address",
                    )
                )
            except OutOfBoundsError as out_of_bounds_error:
                logger.error(out_of_bounds_error.__traceback__)
                not_valid_points.append(
                    GeocodedPoint(
                        lon=None,
                        lat=None,
                        recognized_lon=None,
                        recognized_lat=None,
                        address=address,
                        recognized_address=None,
                        message="Out Of Bounds",
                    )
                )

    return valid_points, not_valid_points


def extend_lists_in_dict(
    input_dict, desired_length, fill_value=None, exclude_keys=["metadata"]
):
    """
    Extend the lists in a dictionary to the desired length, filling with a specified value.

    Args:
        input_dict (dict): Dictionary with lists to extend.
        desired_length (int): Desired length for the lists.
        fill_value (Any, optional): Value to fill the lists with. Defaults to None.
        exclude_keys (list, optional): Keys to exclude from extending. Defaults to ["metadata"].

    Returns:
        dict: Dictionary with extended lists.
    """
    return {
        k: (
            v + [fill_value] * (desired_length - len(v)) if k not in exclude_keys else v
        )
        for k, v in input_dict.items()
    }


def read_file(file_content: str) -> List[Tuple[float, float, str]]:
    """
    Read CSV file content and extract latitude, longitude, and address.

    Args:
        file_content (str): CSV file content as a string.

    Returns:
        List[Tuple[float, float, str]]: List of tuples containing latitude, longitude, and address.
    """
    csv_data = []
    try:
        file_like = io.StringIO(file_content)
        reader = csv.DictReader(file_like, delimiter="|")

        for row in reader:
            try:
                lat = float(row["lat"]) if row["lat"] else None
                lon = float(row["lon"]) if row["lon"] else None
                address = row["address"] if row["address"] else None
                csv_data.append((lat, lon, address))
            except KeyError as e:
                logger.error(f"Missing column in the CSV: {e}")
            except ValueError as e:
                logger.error(f"Invalid data format in the CSV: {e}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
    except Exception as e:
        logger.error(f"Error reading file: {e}")

    return csv_data


def dict_to_csv(data_dict: Dict) -> str:
    """
    Convert dictionary to CSV string.

    Args:
        data_dict (Dict): Dictionary with data to be converted to CSV.

    Returns:
        str: CSV formatted string.
    """
    csv_buffer = StringIO()
    fieldnames = list(data_dict.keys())
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    csv_writer.writeheader()

    for row in zip(*data_dict.values()):
        row_dict = dict(zip(fieldnames, row))
        csv_writer.writerow(row_dict)

    csv_data = csv_buffer.getvalue()
    csv_buffer.close()
    return csv_data


def write_dict_to_s3_as_csv(csv_data: str, bucket_name: str, file_key: str):
    """
    Write CSV data to S3.

    Args:
        csv_data (str): CSV data as a string.
        bucket_name (str): Name of the S3 bucket.
        file_key (str): S3 object key.
    """
    s3_client = boto3.client("s3")
    try:
        s3_client.put_object(
            Body=csv_data.encode("utf-8"), Bucket=bucket_name, Key=file_key
        )
        logger.info(f"CSV file uploaded successfully to s3://{bucket_name}/{file_key}")
    except Exception as e:
        logger.error(f"Error uploading CSV file to S3: {e}")


def get_s3_parent_folder(s3_path: str) -> str:
    """
    Get the parent folder path from an S3 object key.

    Args:
        s3_path (str): S3 object key.

    Returns:
        str: Parent folder path.
    """
    last_slash_index = s3_path.rfind("/")
    return s3_path[:last_slash_index]


def get_national_average_aal_col(
    land_use_rows: List[str], metadata: dict
) -> List[float]:
    """
    Get national average AAL column from tiff metadata.

    Args:
        land_use_rows (List[str]): List of land use row identifiers.
        metadata (dict): Metadata containing AAL information.

    Returns:
        List[float]: National AAL column rows.
    """
    land_use_rows_names = [
        CLC_MAPPING.get(int(land_use_id), DamageCurveEnum.OTHERS)
        for land_use_id in land_use_rows
    ]

    return [
        metadata[f"Average_{land_use_name}_AAL"]
        for land_use_name in land_use_rows_names
    ]


def get_geocoded_points_attributes(points: List[GeocodedPoint]) -> Dict[str, List[Any]]:
    """
    Get attributes of geocoded points.

    Args:
        points (List[GeocodedPoint]): List of geocoded points.

    Returns:
        Dict[str, List[Any]]: Dictionary with attributes of geocoded points.
    """
    attributes = {
        "latitude": [],
        "longitude": [],
        "recognized_latitude": [],
        "recognized_longitude": [],
        "address": [],
        "recognized_address": [],
        "message": [],
    }

    for point in points:
        attributes["latitude"].append(point.lat)
        attributes["longitude"].append(point.lon)
        attributes["recognized_latitude"].append(point.recognized_lat)
        attributes["recognized_longitude"].append(point.recognized_lon)
        attributes["address"].append(point.address)
        attributes["recognized_address"].append(point.recognized_address)
        attributes["message"].append(point.message)

    return attributes


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


def add_national_average_aal(response: Dict) -> Dict:
    """
    Add national AAL to the response.

    Args:
        response (Dict): Response dictionary.

    Returns:
        Dict: Updated response dictionary with national AAL.
    """
    metadata = response.pop("metadata")
    national_average_aal_col = get_national_average_aal_col(
        response["land_use"], metadata
    )
    response.update({"national_average_aal": national_average_aal_col})
    return response


def add_not_valid_points(
    response: Dict, valid_points: List, not_valid_points: List
) -> Dict:
    """
    Add not valid points to the response and update the points attributes.

    Args:
        response (Dict): Response dictionary.
        valid_points (List): List of valid points.
        not_valid_points (List): List of not valid points.

    Returns:
        Dict: Updated response dictionary.
    """
    valid_points.extend(not_valid_points)
    points_attributes = get_geocoded_points_attributes(valid_points)
    logger.debug(f"Points attributes: {points_attributes}")
    response.update(points_attributes)
    logger.debug(f"Output values: {response}")
    final_response = extend_lists_in_dict(
        response, len(valid_points)
    )  # add None value to each band for every not valid points
    return final_response


def sample_valid_points(file_metadata: Dict, valid_points: List) -> Dict:
    return sample(
        filename=file_metadata["filename"],
        tiff_tags=file_metadata.get(
            "tiff_tags",
            [
                TiffTagsKeys.AGRICULTURE_AAL,
                TiffTagsKeys.COMMERCIAL_AAL,
                TiffTagsKeys.INDUSTRIAL_AAL,
                TiffTagsKeys.INFRASTRUCTURE_AAL,
                TiffTagsKeys.RESIDENTIAL_AAL,
                TiffTagsKeys.NONE_AAL,
            ],
        ),
        coordinates=[
            (
                (
                    geocoded_point.lat
                    if geocoded_point.lat is not None
                    else geocoded_point.recognized_lat
                ),
                (
                    geocoded_point.lon
                    if geocoded_point.lon is not None
                    else geocoded_point.recognized_lon
                ),
                (
                    geocoded_point.address
                    if geocoded_point.address is not None
                    else geocoded_point.recognized_address
                ),
            )
            for geocoded_point in valid_points
        ],
        geodatareader=riogeoreader,
    )


def write_output_to_s3(csv_data_str: str, event: Dict) -> None:
    """
    Write the final response to S3 as a CSV file.

    Args:
        csv_data_str (str): Final response csv string.
        event (Dict): Event dictionary containing S3 information.
    """
    bucket, key = get_bucket_and_key(event)
    file_folder = get_s3_parent_folder(key)
    write_dict_to_s3_as_csv(csv_data_str, bucket, f"{file_folder}/output.csv")


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: Dict, context: Dict = None) -> Dict:
    """
    AWS Lambda handler function to process S3 file upload event.

    Args:
        event (Dict): Event data passed to the Lambda function.
        context (Dict): Context object (optional).

    Returns:
        Dict: Processed response.
    """
    file_content, file_metadata = parse_s3_file_upload_event(event=event)
    csv_data = read_file(file_content)
    valid_points, not_valid_points = separate_valid_points(csv_data, gmapsgeocoder)

    logger.debug(f"Valid points: {valid_points}")
    logger.debug(f"Not valid points: {not_valid_points}")

    response = sample_valid_points(file_metadata, valid_points)

    # Get National AAL from tiff metadata
    response = add_national_average_aal(response)

    # Add not valid points to final result
    response = add_not_valid_points(response, valid_points, not_valid_points)

    # Write output values
    logger.info(f"Writing: \n {response}")
    csv_data_str = dict_to_csv(response)

    # Write on S3
    write_output_to_s3(csv_data_str, event)

    logger.info(f"Returning response: {response}")
    return response
