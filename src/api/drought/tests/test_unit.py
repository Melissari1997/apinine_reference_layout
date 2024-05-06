import main
import pytest
from common.response import FailedGeocodeError
from common.status_codes import StatusCodes
from geocoder.geocoder import Geocoder
from main import DroughtKeys, handler
from readgeodata.interfaces import GeoDataReader


class MockGeocoder(Geocoder):
    def __init__(self) -> None:
        pass

    def geocode(self, address: str) -> tuple[tuple[float, float], str]:
        if address.lower() == "via verruca 1 trento":
            return ((12.215283630441727, 44.88393348245498), "via verruca 1 trento")
        else:
            raise FailedGeocodeError(f"Failed geocoding {address}")


class MockGeoDataReaderDrought(GeoDataReader):
    def sample_data_points(
        self,
        filename: str,
        coordinates: list[tuple],
        metadata: list[str] | None = None,
        coordinates_crs: int = 4326,
    ):
        return {
            DroughtKeys.DURATION_RP20: [0.0],
            DroughtKeys.DURATION_RP100: [0.01],
            DroughtKeys.DURATION_RP200: [0.3],
            DroughtKeys.SEVERITY_RP20: [11.2],
            DroughtKeys.SEVERITY_RP100: [12.3],
            DroughtKeys.SEVERITY_RP200: [15.3],
        }


@pytest.mark.unit
class TestDroughtUnit:
    def test_drought_address(
        self, geotiff_json_mock, event_address, lambda_powertools_ctx, monkeypatch
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderDrought()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        want_status_code = 200
        got = handler(event=event_address, context=lambda_powertools_ctx)

        assert want_status_code == got["statusCode"]

    def test_drought_lat_lon(
        self, geotiff_json_mock, event_lat_lon, lambda_powertools_ctx, monkeypatch
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderDrought()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        want_status_code = 200
        got = handler(event=event_lat_lon, context=lambda_powertools_ctx)

        assert want_status_code == got["statusCode"]

    def test_drought_invalid_address(
        self,
        geotiff_json_mock,
        event_invalid_address,
        lambda_powertools_ctx,
        monkeypatch,
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderDrought()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        want_status_code, wanted_body = StatusCodes.UNKNOWN_ADDRESS

        got = handler(event=event_invalid_address, context=lambda_powertools_ctx)

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_drought_conflicting(
        self,
        geotiff_json_mock,
        event_conflict_lat_lon_addr,
        lambda_powertools_ctx,
        monkeypatch,
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderDrought()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        got = handler(event=event_conflict_lat_lon_addr, context=lambda_powertools_ctx)

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_handler_no_queryparams(
        self, geotiff_json_mock, lambda_powertools_ctx, monkeypatch
    ):
        got = handler(event={}, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]
