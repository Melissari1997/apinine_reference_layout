import json
import os

import pytest


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


@pytest.fixture()
def geotiff_json_baseline():
    yield json.dumps(
        [
            {
                "climate_scenario": "baseline",
                "path": "s3://mlflow-monitoring/101/6d721f826af34c88bbc0e3f70b09e729/artifacts/inference/drought_intensity_rp_20_100_200.tif",
            }
        ]
    )


@pytest.fixture(scope="function")
def geotiff_path_s3(geotiff_json_baseline):

    os.environ["GEOTIFF_JSON"] = geotiff_json_baseline
    os.environ["GMAPS_SECRET_NAME"] = "apinine/gmaps_apikey"
    os.environ["GMAPS_SECRET_REGION"] = "eu-central-1"

    yield {"GEOTIFF_JSON": geotiff_json_baseline}

    del os.environ["GEOTIFF_JSON"]


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
