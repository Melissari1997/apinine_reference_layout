from io import StringIO
import os

from aws_lambda_powertools import Logger, Tracer
from common.event_parser import (
    get_bucket_and_key,
    parse_aws_event,
    parse_s3_file_upload_event,
)
from common.input_schema import RiskInputSchema
from common.parse_env import BaselineEnvParser
from common.response import handle_response
from geocoder.gmaps_geocoder import GMapsGeocoder
from main import main
from readgeodata.rasterioreader import RasterIOReader
from schema import OutputSchema
import csv
import boto3

logger = Logger()
tracer = Tracer()
gmapsgeocoder = GMapsGeocoder()
riogeoreader = RasterIOReader()


def dict_to_csv(data_dict: dict) -> str:
    # Create a CSV string from the dictionary
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)

    # Write header
    header = list(data_dict.keys())
    csv_writer.writerow(header)

    # Write rows
    for row in zip(*data_dict.values()):
        csv_writer.writerow(row)

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


def get_s3_parent_folder(s3_path):
    # Find the index of the last '/'
    last_slash_index = s3_path.rfind("/")

    # Extract the path up to the last '/'
    folder_path = s3_path[:last_slash_index]

    return folder_path


@handle_response(validate_schema=OutputSchema)
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event: dict, context: dict = None) -> dict:
    file_content, file_metadata = parse_s3_file_upload_event(event=event)
    csv_reader = csv.reader(StringIO(file_content))
    csv_data = []
    for row in csv_reader:
        if len(row) == 3:
            csv_data.append((row[0], row[1], row[2]))
            # (lat, lon, address)
        else:
            print(f"Number of columns != 3: {len(row)}")

    response = main(
        filename=file_metadata["filename"],
        tiff_metadata=file_metadata["tags"],
        coordinates=csv_data,
        geocoder=gmapsgeocoder,
        geodatareader=riogeoreader,
    )

    csv_data = dict_to_csv(response)
    bucket, key = get_bucket_and_key(event)
    file_folder = get_s3_parent_folder(key)
    write_dict_to_s3_as_csv(csv_data, bucket, f"{file_folder}/output.csv")

    logger.info(f"Returning response: {response}")
    return response
