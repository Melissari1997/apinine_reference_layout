import main
import pytest
from common.response import FailedGeocodeError
from common.status_codes import StatusCodes
from geocoder.geocoder import Geocoder
from main import WildfireKeys, handler
from readgeodata.interfaces import GeoDataReader


class MockGeocoder(Geocoder):
    def __init__(self) -> None:
        pass

    def geocode(self, address: str) -> tuple[tuple[float, float], str]:
        if address.lower() == "via verruca 1 trento":
            return ((12.215283630441727, 44.88393348245498), "via verruca 1 trento")
        else:
            raise FailedGeocodeError(f"Failed geocoding {address}")


class MockGeoDataReaderFlood(GeoDataReader):
    def sample_data_points(
        self,
        filename: str,
        coordinates: list[tuple],
        metadata: list[str],
        coordinates_crs: int = 4326,
    ):
        return {
            WildfireKeys.FWI_2: [0.0],
            WildfireKeys.FWI_10: [0.01],
            WildfireKeys.FWI_30: [0.3],
        }


@pytest.mark.unit
class TestWildfireUnit:
    def test_wildfire_address(
        self, geotiff_path_s3, event_address, lambda_powertools_ctx, monkeypatch
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderFlood()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        want_status_code = 200
        got = handler(event=event_address, context=lambda_powertools_ctx)

        assert want_status_code == got["statusCode"]

    def test_wildfire_lat_lon(
        self, geotiff_path_s3, event_lat_lon, lambda_powertools_ctx, monkeypatch
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderFlood()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        want_status_code = 200
        got = handler(event=event_lat_lon, context=lambda_powertools_ctx)

        assert want_status_code == got["statusCode"]

    def test_wildfire_invalid_address(
        self, geotiff_path_s3, event_invalid_address, lambda_powertools_ctx, monkeypatch
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderFlood()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        want_status_code, wanted_body = StatusCodes.UNKNOWN_ADDRESS

        got = handler(event=event_invalid_address, context=lambda_powertools_ctx)

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_wildfire_conflicting(
        self,
        geotiff_path_s3,
        event_conflict_lat_lon_addr,
        lambda_powertools_ctx,
        monkeypatch,
    ):
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderFlood()
        monkeypatch.setattr(main, "gmapsgeocoder", gmaps)
        monkeypatch.setattr(main, "riogeoreader", rioreader)

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        got = handler(event=event_conflict_lat_lon_addr, context=lambda_powertools_ctx)

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]
