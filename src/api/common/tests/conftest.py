import json

import pytest


@pytest.fixture(scope="function")
def querystring_table():
    yield {}


@pytest.fixture()
def geotiff_baseline():
    yield [
        {
            "climate_scenario": "baseline",
            "path": "my/s3/path.tif",
        }
    ]


@pytest.fixture()
def geotiff_json_baseline(geotiff_baseline):
    yield json.dumps(geotiff_baseline)


@pytest.fixture()
def geotiff_rcp():
    yield [
        {
            "climate_scenario": "rcp26",
            "year": "2030",
            "path": "my/s3/path_2030.tif",
        },
        {
            "climate_scenario": "rcp26",
            "year": "2040",
            "path": "my/s3/path_2040.tif",
        },
        {
            "climate_scenario": "rcp26",
            "year": "2050",
            "path": "my/s3/path_2050.tif",
        },
        {
            "climate_scenario": "rcp26",
            "year": "2060",
            "path": "my/s3/path_2060.tif",
        },
    ]


@pytest.fixture()
def geotiff_json_rcp(geotiff_rcp):
    yield json.dumps(geotiff_rcp)
