from io import StringIO
from typing import List, Tuple

from aws_lambda_powertools import Logger, Tracer
from common.event_parser import (
    get_bucket_and_key,
    parse_s3_file_upload_event,
)
from geocoder.gmaps_geocoder import GMapsGeocoder
from main import main
from readgeodata.rasterioreader import RasterIOReader
import csv
import boto3
import io
import numpy as np

logger = Logger()
tracer = Tracer()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


def convert_ndarrays_to_lists(data_dict: dict) -> dict:
    """Convert ndarray values in the dictionary to lists."""
    for key in data_dict:
        if isinstance(data_dict[key], np.ndarray):
            data_dict[key] = data_dict[key].tolist()
    return data_dict


def read_file(file_content):

    csv_data = []
    try:
        # Convert file content to a file-like object
        file_like = io.StringIO(file_content)
        reader = csv.DictReader(file_like, delimiter="|", quoting=csv.QUOTE_NONNUMERIC)

        for row in reader:
            try:
                # Extract the selected columns
                lat = float(row["lat"])
                lon = float(row["lon"])
                address = row["address"]
                csv_data.append((lat, lon, address))
            except KeyError as e:
                print(f"Missing column in the CSV: {e}")
            except ValueError as e:
                print(f"Invalid data format in the CSV: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
    except Exception as e:
        print(f"Error reading file: {e}")

    return csv_data


def dict_to_csv(data_dict: dict) -> str:
    # Create a CSV string from the dictionary
    csv_buffer = StringIO()

    # Get the field names (keys of the dictionary)
    fieldnames = list(data_dict.keys())

    # Create a DictWriter object, with the field names
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)

    # Write the header
    csv_writer.writeheader()

    # Write the rows
    for row in zip(*data_dict.values()):
        row_dict = dict(zip(fieldnames, row))
        csv_writer.writerow(row_dict)

    # Get CSV data as string
    csv_data = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_data


def write_dict_to_s3_as_csv(csv_data, bucket_name: str, file_key: str):

    # Initialize S3 client
    s3_client = boto3.client("s3")

    try:
        # Upload CSV data to S3
        s3_client.put_object(
            Body=csv_data.encode("utf-8"), Bucket=bucket_name, Key=file_key
        )
        print(f"CSV file uploaded successfully to s3://{bucket_name}/{file_key}")
    except Exception as e:
        print(f"Error uploading CSV file to S3: {e}")


def split_coordinates(coordinates: List[Tuple[str, str, str]]):
    points_array = np.array(coordinates)

    # Split the array into two separate arrays
    latitudes = points_array[:, 0]
    longitudes = points_array[:, 1]
    addresses = points_array[:, 2]

    # Convert numpy arrays back to lists
    latitudes_list = latitudes.tolist()
    longitudes_list = longitudes.tolist()
    addresses_list = addresses.tolist()

    return latitudes_list, longitudes_list, addresses_list


def get_s3_parent_folder(s3_path):
    # Find the index of the last '/'
    last_slash_index = s3_path.rfind("/")

    # Extract the path up to the last '/'
    folder_path = s3_path[:last_slash_index]

    return folder_path


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: dict = None) -> dict:
    file_content, file_metadata = parse_s3_file_upload_event(event=event)
    csv_data = read_file(file_content)
    response = main(
        filename=file_metadata["filename"],
        tiff_metadata=file_metadata.get("tags", []),
        coordinates=csv_data,
        geocoder=gmapsgeocoder,
        geodatareader=riogeoreader,
    )

    response.pop("metadata")
    logger.info(f"Result: {response}")

    converted_response = convert_ndarrays_to_lists(response)

    latitudes, longitudes, addresses = split_coordinates(csv_data)

    converted_response["latitude"] = latitudes
    converted_response["longitude"] = longitudes
    converted_response["addresses"] = addresses

    logger.info(f"Writing: \n {converted_response}")
    csv_data = dict_to_csv(converted_response)
    bucket, key = get_bucket_and_key(event)
    file_folder = get_s3_parent_folder(key)
    write_dict_to_s3_as_csv(csv_data, bucket, f"{file_folder}/output.csv")

    logger.info(f"Returning response: {response}")
    return response
