import json
import os

import pytest


class ContextMock:
    def __init__(self) -> None:
        self.function_name = "lambda_handler"
        self.memory_limit_in_mb = 512
        self.invoked_function_arn = "ARN"
        self.aws_request_id = "111111111111"


@pytest.fixture(scope="function")
def lambda_powertools_ctx():
    yield ContextMock()


@pytest.fixture()
def geotiff_json_baseline():
    yield json.dumps(
        [
            {
                "climate_scenario": "baseline",
                "path": "s3://mlflow-monitoring/112/b66c45f2f2ad4757bff0ba886cbc724d/artifacts/inference/baseline_with_risk_index.tif",
            }
        ]
    )


@pytest.fixture(scope="function")
def geotiff_path_s3(geotiff_json_baseline):

    os.environ["GEOTIFF_JSON"] = geotiff_json_baseline

    yield {"GEOTIFF_JSON": geotiff_json_baseline}

    del os.environ["GEOTIFF_JSON"]
