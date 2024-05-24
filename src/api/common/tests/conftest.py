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


@pytest.fixture(scope="function")
def event_address():
    yield {"queryStringParameters": {"address": "via verruca 1 trento"}}


@pytest.fixture(scope="function")
def event_address_rcp(event_address):
    event_address["queryStringParameters"]["year"] = "2040"
    yield event_address
