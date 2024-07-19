import pytest
from moto import mock_aws
import boto3


@pytest.fixture(scope="function")
def event_new_file_uploaded():
    yield {
        "version": "0",
        "id": "",
        "detail-type": "Object Created",
        "source": "",
        "account": "",
        "time": "",
        "region": "eu-central-1",
        "resources": ["arn:aws:s3:::eoliann-batch-input"],
        "detail": {
            "version": "0",
            "bucket": {"name": "test-bucket-setup"},
            "object": {
                "key": "mock_file.csv",
                "size": 1708,
                "etag": "",
                "sequencer": "",
            },
            "request-id": "",
            "requester": "",
            "source-ip-address": "",
            "reason": "PutObject",
        },
    }


class ContextMock:
    def __init__(self) -> None:
        self.function_name = "lambda_handler"
        self.memory_limit_in_mb = 512
        self.invoked_function_arn = "ARN"
        self.aws_request_id = "111111111111"


@pytest.fixture(scope="function")
def lambda_powertools_ctx():
    yield ContextMock()
