import json

import pytest
from baseline.handler import handler as baseline_handler
from common.status_codes import StatusCodes
from geocoder.gmaps_geocoder import GMapsGeocoder
from main import main
from rcp.handler import handler as rcp_handler
from readgeodata.rasterioreader import RasterIOReader


# Real calls to gmaps and aws
@pytest.mark.integration
class TestFloodIntegrationMain:
    def test_integ_main(self, geotiff_path_s3):
        lon, lat = 12.215283630441727, 44.88393348245498
        gmaps = GMapsGeocoder()
        rioreader = RasterIOReader()
        filename = json.loads(geotiff_path_s3["GEOTIFF_JSON"])[0]["path"]
        got = main(
            filename=filename,
            address=None,
            lon=lon,
            lat=lat,
            geocoder=gmaps,
            geodatareader=rioreader,
        )

        # Checking only format and types, not the values
        assert isinstance(got, dict)


@pytest.mark.integration
@pytest.mark.parametrize(
    "handler",
    [baseline_handler, rcp_handler],
)
class TestFloodIntegrationHandler:
    def test_integ_handler_address(
        self, handler, geotiff_path_s3, lambda_powertools_ctx, event_address
    ):
        got = handler(event=event_address, context=lambda_powertools_ctx)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_integ_handler_output(
        self, handler, geotiff_path_s3, lambda_powertools_ctx, event_address
    ):
        got = handler(event=event_address, context=lambda_powertools_ctx)

        keys_want = {
            "address",
            "lat",
            "lon",
            "land_use",
            "flood_risk_assessment",
            "risk_index",
            "average_annual_loss",
            "hazard_index",
        }

        assert set(json.loads(got["body"])) == keys_want

    def test_integ_handler_missing_filename(
        self, handler, event_address, lambda_powertools_ctx
    ):
        got = handler(event=event_address, context=lambda_powertools_ctx)

        want_status_code = 500
        wanted_body = "Internal Server Error"

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_handler_lat_lon(
        self, handler, geotiff_path_s3, event_lat_lon, lambda_powertools_ctx
    ):
        got = handler(event=event_lat_lon, context=lambda_powertools_ctx)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_integ_handler_invalid_lat_lon(
        self, handler, geotiff_path_s3, event_invalid_lat_lon, lambda_powertools_ctx
    ):
        got = handler(event=event_invalid_lat_lon, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.MISSING_DATA

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_handler_conflict(
        self,
        handler,
        geotiff_path_s3,
        event_conflict_lat_lon_addr,
        lambda_powertools_ctx,
    ):
        got = handler(event=event_conflict_lat_lon_addr, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_invalid_address(
        self, handler, geotiff_path_s3, event_invalid_address, lambda_powertools_ctx
    ):
        got = handler(event=event_invalid_address, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.UNKNOWN_ADDRESS

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_oob_address(
        self, handler, geotiff_path_s3, event_oob_address, lambda_powertools_ctx
    ):
        got = handler(event=event_oob_address, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.OUT_OF_BOUNDS

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    #  2024-03-04: commented because google maps does not
    #   reply anymore with multiple addresses in this scenario
    # def test_integ_too_generic_address(
    #    self, geotiff_path_s3, event_too_generic_address, lambda_powertools_ctx
    # ):
    #    got = handler(event=event_too_generic_address, context=lambda_powertools_ctx)
    #
    #    want_status_code, wanted_body = StatusCodes.UNKNOWN_ADDRESS
    #
    #    assert want_status_code == got["statusCode"]
    #    assert wanted_body == got["body"]
