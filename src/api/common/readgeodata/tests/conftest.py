import json
import os

import pytest
from geocoder.geocoder import Geocoder
from readgeodata.interfaces import GeoDataReader


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
def geotiff_env_baseline(geotiff_json_baseline):

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
    yield {"queryStringParameters": {"address": "via 12345676789poiuyttr"}}


@pytest.fixture(scope="function")
def event_lat_lon():
    yield {"queryStringParameters": {"lat": "46.0701698", "lon": "11.1135156"}}


@pytest.fixture(scope="function")
def event_invalid_lat_lon():
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


class MockGeocoder(Geocoder):
    def __init__(self) -> None:
        pass

    def geocode(self, address: str) -> tuple[tuple[float, float], str]:
        return ((12.215283630441727, 44.88393348245498), "via verruca 1 trento")


@pytest.fixture()
def mockgeocoder():
    yield MockGeocoder()


class MockGeoDataReaderFlood(GeoDataReader):
    def sample_data_points(
        self,
        filename: str,
        coordinates: list[tuple],
        metadata: list[str],
        coordinates_crs: int = 4326,
    ):
        return {
            FloodKeys.LAND_USE: [112],
            FloodKeys.WH_20: [0.0],
            FloodKeys.WH_100: [0.01],
            FloodKeys.WH_200: [0.3],
            FloodKeys.VULN_20: [0.0],
            FloodKeys.VULN_100: [0.0001],
            FloodKeys.VULN_200: [0.56],
            FloodKeys.RISK_INDEX: [2],
            FloodKeys.AAL: [0.032],
            "metadata": {
                FloodKeys.NATIONAL_AAL: 0.0035,
                FloodKeys.AGRICULTURE_AAL: 0.0036,
                FloodKeys.RESIDENTIAL_AAL: 0.0034,
            },
        }


@pytest.fixture()
def mockgeodatareaderflood():
    yield MockGeoDataReaderFlood()


# RCP


@pytest.fixture()
def geotiff_json_rcp():
    yield json.dumps(
        [
            {
                "climate_scenario": "rcp45",
                "year": "2030",
                "path": "s3://mlflow-monitoring/112/2caafa97230a4ec19c928e400b6fcd32/artifacts/inference/rcp4.5_2030_IT.tif",
            },
            {
                "climate_scenario": "rcp45",
                "year": "2040",
                "path": "s3://mlflow-monitoring/112/2caafa97230a4ec19c928e400b6fcd32/artifacts/inference/rcp4.5_2040_IT.tif",
            },
            {
                "climate_scenario": "rcp45",
                "year": "2050",
                "path": "s3://mlflow-monitoring/112/2caafa97230a4ec19c928e400b6fcd32/artifacts/inference/rcp4.5_2050_IT.tif",
            },
        ]
    )


@pytest.fixture(scope="function")
def geotiff_env_rcp(geotiff_json_rcp):

    os.environ["GEOTIFF_JSON"] = geotiff_json_rcp
    os.environ["GMAPS_SECRET_NAME"] = "apinine/gmaps_apikey"
    os.environ["GMAPS_SECRET_REGION"] = "eu-central-1"

    yield {"GEOTIFF_JSON": geotiff_json_rcp}

    del os.environ["GEOTIFF_JSON"]


@pytest.fixture(scope="function")
def event_address_rcp(event_address):
    event_address["queryStringParameters"]["year"] = "2040"
    yield event_address


@pytest.fixture(scope="function")
def event_invalid_address_rcp(event_invalid_address):
    event_invalid_address["queryStringParameters"]["year"] = "2040"
    yield event_invalid_address


@pytest.fixture(scope="function")
def event_lat_lon_rcp(event_lat_lon):
    event_lat_lon["queryStringParameters"]["year"] = "2040"
    yield event_lat_lon


@pytest.fixture(scope="function")
def event_invalid_lat_lon_rcp(event_invalid_lat_lon):
    event_invalid_lat_lon["queryStringParameters"]["year"] = "2040"
    yield event_invalid_lat_lon


@pytest.fixture(scope="function")
def event_too_generic_address_rcp(event_too_generic_address):
    event_too_generic_address["queryStringParameters"]["year"] = "2040"
    yield event_too_generic_address


@pytest.fixture(scope="function")
def event_oob_address_rcp(event_oob_address):
    event_oob_address["queryStringParameters"]["year"] = "2040"
    yield event_oob_address


@pytest.fixture(scope="function")
def event_conflict_lat_lon_addr_rcp(event_conflict_lat_lon_addr):
    event_conflict_lat_lon_addr["queryStringParameters"]["year"] = "2040"
    yield event_conflict_lat_lon_addr


@pytest.fixture(scope="function")
def event_invalid_lat_lon_values_rcp(event_invalid_lat_lon_values):
    event_invalid_lat_lon_values["queryStringParameters"]["year"] = "2040"
    yield event_invalid_lat_lon_values


@pytest.fixture(scope="function")
def event_invalid_year(event_address):
    event_address["queryStringParameters"]["year"] = "1984"
    yield event_address
