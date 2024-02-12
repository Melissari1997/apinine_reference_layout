import pytest
from common.status_codes import StatusCodes
from geocoder.gmaps_geocoder import GMapsGeocoder
from main import handler, main
from readgeodata.rasterioreader import RasterIOReader


# Real calls to gmaps and aws
@pytest.mark.integration
class TestFloodIntegration:
    def test_integ_main(self, geotiff_path_s3):
        lon, lat = 12.215283630441727, 44.88393348245498
        gmaps = GMapsGeocoder()
        rioreader = RasterIOReader()
        got = main(
            filename=geotiff_path_s3["GEOTIFF_PATH"],
            address=None,
            lon=lon,
            lat=lat,
            geocoder=gmaps,
            geodatareader=rioreader,
        )

        # Checking only format and types, not the values
        assert isinstance(got, dict)

    def test_integ_handler_address(self, geotiff_path_s3, event_address):
        got = handler(event=event_address, context=None)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_integ_handler_missing_filename(self, event_address):
        got = handler(event=event_address, context=None)

        want_status_code = 500
        wanted_body = "Internal Server Error"

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_handler_lat_lon(self, geotiff_path_s3, event_lat_lon):
        got = handler(event=event_lat_lon, context=None)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_integ_handler_invalid_lat_lon(
        self, geotiff_path_s3, event_invalid_lat_lon
    ):
        got = handler(event=event_invalid_lat_lon, context=None)

        want_status_code, wanted_body = StatusCodes.MISSING_DATA

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_handler_conflict(self, geotiff_path_s3, event_conflict_lat_lon_addr):
        got = handler(event=event_conflict_lat_lon_addr, context=None)

        want_status_code, wanted_body = StatusCodes.CONFLICTING_INPUTS

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_invalid_address(self, geotiff_path_s3, event_invalid_address):
        got = handler(event=event_invalid_address, context=None)

        want_status_code, wanted_body = StatusCodes.UNKNOWN_ADDRESS

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_oob_address(self, geotiff_path_s3, event_oob_address):
        got = handler(event=event_oob_address, context=None)

        want_status_code, wanted_body = StatusCodes.OUT_OF_BOUNDS

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_too_generic_address(
        self, geotiff_path_s3, event_too_generic_address
    ):
        got = handler(event=event_too_generic_address, context=None)

        want_status_code, wanted_body = StatusCodes.UNKNOWN_ADDRESS

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]