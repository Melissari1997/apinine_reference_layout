import os

import pytest


@pytest.fixture(scope="function")
def geotiff_path_s3():
    geotiff_path = "s3://mlflow-monitoring/93/cf7509a33fe543a9a87aa7658e551659/artifacts/inference/aal_baseline_8bands.tif"
    os.environ["GEOTIFF_PATH"] = geotiff_path

    yield {"GEOTIFF_PATH": geotiff_path}

    del os.environ["GEOTIFF_PATH"]


@pytest.fixture(scope="function")
def event_address():
    yield {"queryStringParameters": {"address": "via verruca 1 trento"}}


@pytest.fixture(scope="function")
def event_lat_lon():
    yield {"queryStringParameters": {"lat": 45.26464, "lon": 12.57188}}
