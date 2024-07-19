import pytest
import boto3
from io import BytesIO
from handler import read_file
from common.event_parser import get_bucket_and_key, parse_s3_file_upload_event
from moto import mock_aws
import handler as handler_module


@mock_aws
@pytest.mark.unit
def test_parse_s3_file_upload_event_and_process(
    event_new_file_uploaded, lambda_powertools_ctx, monkeypatch
):
    # Set up the mock S3 environment
    conn = boto3.client("s3", region_name="us-east-1")
    monkeypatch.setenv("GMAPS_SECRET_NAME", "apinine/gmaps_apikey")
    monkeypatch.setenv("GMAPS_SECRET_REGION", "eu-central-1")

    # Create a bucket and put a file in it
    bucket = "test-bucket-setup"
    key = "mock_file.csv"
    conn.create_bucket(Bucket=bucket)
    local_file_path = "/home/paolo/apinine_reference_layout/src/api/batch/tests/fixtures/mock_input_with_just_coords.csv"
    with open(local_file_path, "r") as f:
        local_file_content = f.read()
    conn.put_object(Bucket=bucket, Key=key, Body=local_file_content)
    tags = {
        "filename": "/home/paolo/apinine_reference_layout/src/api/batch/tests/fixtures/baseline_IT.tif"
    }
    conn.put_object_tagging(
        Bucket=bucket,
        Key=key,
        Tagging={"TagSet": [{"Key": k, "Value": v} for k, v in tags.items()]},
    )

    response = handler_module.handler(
        event=event_new_file_uploaded, context=lambda_powertools_ctx
    )
    print(response)

    # Checking only format and types, not the values
    assert isinstance(response, dict)
