import json
import os
from typing import Dict, List

import boto3
from aws_lambda_powertools import Logger, Tracer
from functions import TIFF_TAGS, hexdigest, list_to_csv, write_batch_input_to_s3

logger = Logger()
tracer = Tracer()


@tracer.capture_method
def main(filename: str, locations: List[Dict], bucket_name: str, body: bytes) -> dict:
    # Tags for S3 file
    tags = f"filename={filename}&tiff-tags={':'.join(TIFF_TAGS)}"

    # Generate body hash - unique if couple (input data, tags) is unique
    digest = hexdigest(bdata=json.dumps(locations).encode(), tags=tags.encode())

    # Assume that all dictionaries have the same keys since they have been validated with the same schema
    fieldnames = locations[0].keys()

    # Upload the file - do nothing if it already exists
    csv_data = list_to_csv(locations, fieldnames=fieldnames)

    # Initialize S3 client
    s3_client = boto3.client("s3")

    # TODO: upload data to an organization-specific s3 path
    # Write input CSV file
    write_batch_input_to_s3(
        s3_client=s3_client,
        bdata=csv_data.encode(),
        bucket_name=bucket_name,
        bdata_key=f"{digest}/input.csv",
        body=body,
        body_key=f"{digest}/body.json",
        tags=tags,
    )

    # return response
    return {
        "id": digest,
        "links": {
            "status": f"https://{os.environ['DOMAIN_NAME']}/flood/v1/batch/status",  # TODO: insert real endpoint
        },
    }
