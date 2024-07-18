import json
import os

import boto3
import pytest
from moto import mock_aws


class ContextMock:
    def __init__(self) -> None:
        self.function_name = "lambda_handler"
        self.memory_limit_in_mb = 512
        self.invoked_function_arn = "ARN"
        self.aws_request_id = "111111111111"


@pytest.fixture(scope="function")
def lambda_powertools_ctx():
    yield ContextMock()


@pytest.fixture(scope="function")
def setup_env():
    os.environ["DOMAIN_NAME"] = "eoliann.testapi.solutions"
    yield
    del os.environ["DOMAIN_NAME"]


@pytest.fixture()
def geotiff_json_baseline_mock():
    yield json.dumps(
        [
            {
                "climate_scenario": "baseline",
                "path": "my/s3/path.tif",
            }
        ]
    )


@pytest.fixture(scope="function")
def geotiff_json_mock(geotiff_json_baseline_mock):
    os.environ["GEOTIFF_JSON"] = geotiff_json_baseline_mock
    yield {"GEOTIFF_JSON": geotiff_json_baseline_mock}
    del os.environ["GEOTIFF_JSON"]


@pytest.fixture(scope="function")
def mocked_bucket():
    with mock_aws():
        bucket_name = "fakebucket"
        conn = boto3.resource("s3", region_name="us-east-1")
        conn.create_bucket(Bucket=bucket_name)
        yield bucket_name
