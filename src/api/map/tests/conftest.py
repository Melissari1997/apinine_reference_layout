import os
import pathlib

import pytest
from bream.image import raster2 as brast

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
def flood_rcp_geotiff_json():
    json_path = flood_map_path / "rcp" / "build-env-variables.json"
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


@pytest.fixture(scope="function")
def box_3035_verruca():
    box_size = 50
    yield brast.MakeBox.from_point_and_size(
        coords=(11.1135156, 46.0701698),
        coords_crs=4326,
        output_crs=3035,
        width=box_size,
        height=box_size,
    )


@pytest.fixture(scope="function")
def box_3035_lima():
    box_size = 50
    yield brast.MakeBox.from_point_and_size(
        coords=(-77.07344188385699, -12.0571910705544),
        coords_crs=4326,
        output_crs=3035,
        width=box_size,
        height=box_size,
    )
