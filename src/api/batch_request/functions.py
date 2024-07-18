import csv
import hashlib
from io import StringIO
from typing import Dict, List

import botocore
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()


# TODO: move these to build-env-variables.json. This way each tiff can be associated with its tags
TIFF_TAGS = [
    "Average_Agriculture_AAL",
    "Average_Commercial_AAL",
    "Average_Industrial_AAL",
    "Average_Infrastructure_AAL",
    "Average_Residential_AAL",
    "Average_None_AAL",
]


def list_to_csv(data: List[Dict], fieldnames: List, delimiter: str = "|") -> str:
    # Create a CSV string from the dictionary
    csv_buffer = StringIO()

    csv_writer = csv.DictWriter(
        csv_buffer,
        fieldnames=fieldnames,
        delimiter=delimiter,
        quoting=csv.QUOTE_NONNUMERIC,
    )

    csv_writer.writeheader()
    csv_writer.writerows(data)

    # Get CSV data as string
    csv_data = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_data


def write_batch_input_to_s3(
    s3_client,
    bdata: bytes,
    body: bytes,
    bucket_name: str,
    bdata_key: str,
    body_key: str,
    tags: str,
) -> None:
    """Write binary data to s3.

    The logic is the following:
    1. Check for the existence of the file s3://{bucket_name}/{bdata_key}
    2. If it exists, return.
    3. Otherwise:
    3.1 Upload 'bdata' to S3 at path          -> s3://{bucket_name}/{bdata_key}
    3.1 Upload 'body' to S3 at path           -> s3://{bucket_name}/{body_key}

    Parameters
    ----------
    s3_client
        Boto3 S3 client
    bdata : bytes
        CSV-formatted file containing input to batch async task
    body : bytes
        body of the current http request
    bucket_name : str
        S3 bucket to upload data to
    bdata_key : str
        S3 key to upload 'bdata' to
    body_key : str
        S3 key to upload 'body' to
    tags : str
        Tags to attach to bdata file
    """
    try:
        s3_client.head_object(Bucket=bucket_name, Key=bdata_key)
        logger.warning(
            f"File 's3://{bucket_name}/{bdata_key}' already exists - exiting"
        )
        return
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] != "404":
            raise

    # If the file does not exists, upload it
    s3_client.put_object(Body=bdata, Bucket=bucket_name, Key=bdata_key, Tagging=tags)
    logger.info(
        f"File uploaded successfully to 's3://{bucket_name}/{bdata_key}' with tags '{tags}'"
    )

    # And upload request body
    s3_client.put_object(Body=body, Bucket=bucket_name, Key=body_key)
    logger.info(f"File uploaded successfully to 's3://{bucket_name}/{body_key}'")


def hexdigest(bdata: bytes, tags: bytes, algorithm: str = "sha1") -> str:
    sha1 = hashlib.new(algorithm)
    sha1.update(bdata)
    sha1.update(tags)
    return sha1.hexdigest()
