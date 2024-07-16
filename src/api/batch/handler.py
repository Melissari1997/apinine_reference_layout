from io import StringIO
from typing import List, Tuple, Dict

from aws_lambda_powertools import Logger, Tracer
from readgeodata.sampler import sample
from common.event_parser import (
    get_bucket_and_key,
    parse_s3_file_upload_event,
)
from geocoder.gmaps_geocoder import GMapsGeocoder
from readgeodata.rasterioreader import RasterIOReader
import csv
import boto3
import io

# Initialize Logger, Tracer, Geocoder, and GeoReader
logger = Logger()
tracer = Tracer()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


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
        reader = csv.DictReader(file_like, delimiter="|", quoting=csv.QUOTE_NONNUMERIC)

        for row in reader:
            try:
                lat = float(row["lat"])
                lon = float(row["lon"])
                address = row["address"]
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

    response = sample(
        filename=file_metadata["filename"],
        tiff_metadata=file_metadata.get("tags", []),
        coordinates=csv_data,
        geocoder=gmapsgeocoder,
        geodatareader=riogeoreader,
    )
    response.pop("metadata", None)

    logger.info(f"Writing: \n {response}")
    csv_data_str = dict_to_csv(response)
    bucket, key = get_bucket_and_key(event)
    file_folder = get_s3_parent_folder(key)
    write_dict_to_s3_as_csv(csv_data_str, bucket, f"{file_folder}/output.csv")

    logger.info(f"Returning response: {response}")
    return response
