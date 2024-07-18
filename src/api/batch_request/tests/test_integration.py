import csv
import json
import os
import time
from io import StringIO

import boto3
import pytest
from common.status_codes import StatusCodes
from flood.baseline.handler import handler
from functions import TIFF_TAGS
from moto import mock_aws
from schema import BATCH_MAX_SIZE


# These are not unit tests, but are completely mocked and I want CI to run them
@pytest.mark.unit
class TestHandler:
    @mock_aws
    def test_handler(
        self, geotiff_json_mock, lambda_powertools_ctx, mocked_bucket, setup_env
    ):
        locations = {
            "locations": [
                {"lat": 46.07 + 0.0001 * i, "lon": 11.11 + 0.0001 * i}
                for i in range(30)
            ]
        }
        event = {"body": json.dumps(locations)}

        os.environ["S3_BUCKET_NAME"] = mocked_bucket

        # Invoke handler
        response = handler(event=event, context=lambda_powertools_ctx)

        # Check that the file exists
        digest = json.loads(response["body"])["id"]
        client = boto3.client("s3", region_name="us-east-1")
        aws_response = client.get_object(
            Bucket=mocked_bucket, Key=f"{digest}/input.csv"
        )

        # Check file tags
        assert aws_response["TagCount"] == 2
        tags = client.get_object_tagging(
            Bucket=mocked_bucket, Key=f"{digest}/input.csv"
        )["TagSet"]
        assert {
            "Key": "filename",
            "Value": json.loads(geotiff_json_mock["GEOTIFF_JSON"])[0]["path"],
        } in tags

        assert {
            "Key": "tiff-tags",
            "Value": ":".join(TIFF_TAGS),
        } in tags

        # Check the file's content is what we expect
        csv_data = aws_response["Body"].read()
        want = [{"address": "", **location} for location in locations["locations"]]

        reader = csv.DictReader(
            StringIO(csv_data.decode()), delimiter="|", quoting=csv.QUOTE_NONNUMERIC
        )
        got = list(reader)
        assert got == want

        # Check that request body has been correctly written to the bucket
        body = client.get_object(Bucket=mocked_bucket, Key=f"{digest}/body.json")[
            "Body"
        ].read()
        assert body.decode() == json.dumps(locations)

    def test_handler_file_already_exists(
        self, geotiff_json_mock, lambda_powertools_ctx, mocked_bucket, setup_env
    ):
        # I expect that if I invoke the lambda a second time with the same data and tiff file,
        # The function does not upload anything and leaves the existing file as-is
        locations = {
            "locations": [
                {"lat": 46.07 + 0.0001 * i, "lon": 11.11 + 0.0001 * i}
                for i in range(30)
            ]
        }
        event = {"body": json.dumps(locations)}
        os.environ["S3_BUCKET_NAME"] = mocked_bucket
        client = boto3.client("s3", region_name="us-east-1")

        # Invoke handler a first time
        response1 = handler(event=event, context=lambda_powertools_ctx)
        digest1 = json.loads(response1["body"])["id"]
        aws_response1 = client.get_object(
            Bucket=mocked_bucket, Key=f"{digest1}/input.csv"
        )

        # Wait a second to force "LastModified" timestamps to be different
        # This would apply only if the second invocation modified the file
        time.sleep(1)

        # Invoke handler a second time
        response2 = handler(event=event, context=lambda_powertools_ctx)
        digest2 = json.loads(response2["body"])["id"]
        aws_response2 = client.get_object(
            Bucket=mocked_bucket, Key=f"{digest2}/input.csv"
        )

        # Check that operation digests are equal
        assert digest1 == digest2

        # Check that the file has not been modified
        assert aws_response1["LastModified"] == aws_response2["LastModified"]
        assert aws_response1["TagCount"] == aws_response2["TagCount"]

        # The entity tag is a hash of the object.
        # The ETag reflects changes only to the contents of an object, not its metadata.
        assert aws_response1["ETag"] == aws_response2["ETag"]

        # Check that file content is equal
        got1 = aws_response1["Body"].read()
        got2 = aws_response2["Body"].read()

        assert got1 == got2

        # Check that request body has been correctly written to the bucket
        body_response1 = client.get_object(
            Bucket=mocked_bucket, Key=f"{digest1}/body.json"
        )
        body1 = body_response1["Body"].read()

        body_response2 = client.get_object(
            Bucket=mocked_bucket, Key=f"{digest2}/body.json"
        )
        body2 = body_response2["Body"].read()

        # Check that request body did not change
        assert body1.decode() == body2.decode() == json.dumps(locations)
        assert body_response1["LastModified"] == body_response2["LastModified"]

    def test_handler_file_already_exists_but_different_tags(
        self, geotiff_json_mock, lambda_powertools_ctx, mocked_bucket, setup_env
    ):
        # I expect that if I invoke the lambda a second time with the same data but different tags,
        # e.g. different filename, the computed operation digest (hash) will be different, so a new file
        # will be uploaded
        locations = {
            "locations": [
                {"lat": 46.07 + 0.0001 * i, "lon": 11.11 + 0.0001 * i}
                for i in range(30)
            ]
        }
        event = {"body": json.dumps(locations)}
        os.environ["S3_BUCKET_NAME"] = mocked_bucket
        client = boto3.client("s3", region_name="us-east-1")

        # Invoke handler a first time
        response1 = handler(event=event, context=lambda_powertools_ctx)
        digest1 = json.loads(response1["body"])["id"]
        aws_response1 = client.get_object(
            Bucket=mocked_bucket, Key=f"{digest1}/input.csv"
        )

        # Change GEOTIFF_JSON env variable
        os.environ["GEOTIFF_JSON"] = json.dumps(
            [
                {
                    "climate_scenario": "baseline",
                    "path": "a/different/s3/path.tif",
                }
            ]
        )

        # Invoke handler a second time
        response2 = handler(event=event, context=lambda_powertools_ctx)
        digest2 = json.loads(response2["body"])["id"]
        aws_response2 = client.get_object(
            Bucket=mocked_bucket, Key=f"{digest2}/input.csv"
        )

        # Check that operation digests are different
        assert digest1 != digest2

        # In this case, locations are the same so the two files must be equal

        # Check that the files have the same number of tags
        assert aws_response1["TagCount"] == aws_response2["TagCount"]

        # The entity tag is a hash of the object.
        # The ETag reflects changes only to the contents of an object, not its metadata.
        assert aws_response1["ETag"] == aws_response2["ETag"]

        # Check that file content is equal
        got1 = aws_response1["Body"].read()
        got2 = aws_response2["Body"].read()

        assert got1 == got2

    @pytest.mark.parametrize(
        "locations",
        [
            ({}),
            ({"locations": []}),
            (
                {
                    "locations": [
                        {"lat": 46, "lon": 11} for i in range(BATCH_MAX_SIZE + 1)
                    ]
                }
            ),
            (
                {
                    "locations": [
                        {"lat": 46, "lon": 11} for i in range(BATCH_MAX_SIZE + 100)
                    ]
                }
            ),
            ({"locations": [{"lat": 1, "lon": 1}]}),
        ],
    )
    def test_invalid_input(self, geotiff_json_mock, lambda_powertools_ctx, locations):
        event = {"body": json.dumps(locations)}

        response = handler(event=event, context=lambda_powertools_ctx)

        assert response["statusCode"] == StatusCodes.BATCH_REQUEST_INVALID_BODY[0]
        assert response["body"] == StatusCodes.BATCH_REQUEST_INVALID_BODY[1]
