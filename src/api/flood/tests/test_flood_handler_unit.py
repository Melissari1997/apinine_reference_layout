import main
import pytest
from common.status_codes import StatusCodes
from geocoder.geocoder import Geocoder
from main import FloodKeys, handler
from readgeodata.interfaces import GeoDataReader


class MockGeocoder(Geocoder):
    def __init__(self) -> None:
        pass

    def geocode(self, address: str) -> tuple[tuple[float, float], str]:
        return ((12.215283630441727, 44.88393348245498), "via verruca 1 trento")


class MockGeoDataReaderFlood(GeoDataReader):
    def sample_data_points(
        self,
        filename: str,
        coordinates: list[tuple],
        metadata: list[str],
        coordinates_crs: int = 4326,
    ):
        return {
            FloodKeys.WH_20: [0.0],
            FloodKeys.WH_100: [0.01],
            FloodKeys.WH_200: [0.3],
            FloodKeys.VULN_20: [0.0],
            FloodKeys.VULN_100: [0.0001],
            FloodKeys.VULN_200: [0.56],
            FloodKeys.RISK_INDEX: [2],
            FloodKeys.AAL: [0.032],
            "metadata": {FloodKeys.NATIONAL_AAL: 0.045},
        }


@pytest.mark.unit
class TestFloodUnit:
    def test_handler_address(
        self, geotiff_path_s3, event_address, lambda_powertools_ctx, monkeypatch
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderFlood()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        got = handler(event=event_address, context=lambda_powertools_ctx)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_handler_no_queryparams(
        self, geotiff_path_s3, lambda_powertools_ctx, monkeypatch
    ):
        got = handler(event={}, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_handler_lat_lon(
        self, event_lat_lon, geotiff_path_s3, lambda_powertools_ctx, monkeypatch
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderFlood()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        got = handler(event=event_lat_lon, context=lambda_powertools_ctx)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_handler_conflicting(
        self,
        geotiff_path_s3,
        monkeypatch,
        lambda_powertools_ctx,
        event_conflict_lat_lon_addr,
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderFlood()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        got = handler(event=event_conflict_lat_lon_addr, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_invalid_lat_lon(
        self,
        geotiff_path_s3,
        # monkeypatch,
        lambda_powertools_ctx,
        event_invalid_lat_lon_values,
    ):
        got = handler(event=event_invalid_lat_lon_values, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_empty_address(
        self,
        geotiff_path_s3,
        lambda_powertools_ctx,
    ):
        got = handler(
            event={"queryStringParameters": {"address": ""}},
            context=lambda_powertools_ctx,
        )

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]
