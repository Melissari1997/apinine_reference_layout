import os
import pathlib

import pytest

flood_map_path = pathlib.Path(__file__).parent.parent.resolve() / "flood"
wildfire_map_path = pathlib.Path(__file__).parent.parent.resolve() / "wildfire"
drought_map_path = pathlib.Path(__file__).parent.parent.resolve() / "drought"


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
def flood_baseline_geotiff_json():
    json_path = flood_map_path / "baseline" / "build-env-variables.json"
    geotiff_json = open(json_path).read()
    os.environ["GEOTIFF_JSON"] = geotiff_json
    yield geotiff_json
    del os.environ["GEOTIFF_JSON"]


@pytest.fixture(scope="function")
def wildfire_baseline_geotiff_json():
    json_path = wildfire_map_path / "baseline" / "build-env-variables.json"
    geotiff_json = open(json_path).read()
    os.environ["GEOTIFF_JSON"] = geotiff_json
    yield geotiff_json
    del os.environ["GEOTIFF_JSON"]


@pytest.fixture(scope="function")
def drought_baseline_geotiff_json():
    json_path = drought_map_path / "baseline" / "build-env-variables.json"
    geotiff_json = open(json_path).read()
    os.environ["GEOTIFF_JSON"] = geotiff_json
    yield geotiff_json
    del os.environ["GEOTIFF_JSON"]
