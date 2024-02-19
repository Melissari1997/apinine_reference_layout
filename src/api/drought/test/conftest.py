import os

import pytest


@pytest.fixture(scope="function")
def geotiff_path_s3():
    geotiff_path = "s3://mlflow-monitoring/98/14e74db763c74bebaf35d997343f381f/artifacts/inference/placeholder_drought.tif"

    os.environ["GEOTIFF_PATH"] = geotiff_path
    os.environ["GMAPS_SECRET_NAME"] = "apinine/gmaps_apikey"
    os.environ["GMAPS_SECRET_REGION"] = "eu-central-1"

    yield {"GEOTIFF_PATH": geotiff_path}

    del os.environ["GEOTIFF_PATH"]


@pytest.fixture(scope="function")
def event_address():
    yield {"queryStringParameters": {"address": "via verruca 1 trento"}}


@pytest.fixture(scope="function")
def event_invalid_address():
    yield {"queryStringParameters": {"address": "Invalid Address"}}


@pytest.fixture(scope="function")
def event_lat_lon():
    yield {"queryStringParameters": {"lat": "46.0701698", "lon": "11.1135156"}}


@pytest.fixture(scope="function")
def event_invalid_lat_lon():
    # The coords are in the sea
    yield {"queryStringParameters": {"lat": "45.26464", "lon": "12.57188"}}


@pytest.fixture(scope="function")
def event_too_generic_address():
    yield {"queryStringParameters": {"address": "via aurelia"}}


@pytest.fixture(scope="function")
def event_oob_address():
    yield {"queryStringParameters": {"address": "calle santa nicerata lima"}}


@pytest.fixture(scope="function")
def event_conflict_lat_lon_addr():
    yield {
        "queryStringParameters": {
            "lat": "45.26464",
            "lon": "12.57188",
            "address": "via verruca 1 trento",
        }
    }


@pytest.fixture(scope="function")
def event_invalid_lat_lon_values():
    yield {
        "queryStringParameters": {
            "lat": "45555.26464",
            "lon": "12.57188",
        }
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
