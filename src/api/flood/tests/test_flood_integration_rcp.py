import json

import pytest
from common.errors import InvalidYearError
from common.status_codes import StatusCodes
from rcp.handler import handler


@pytest.mark.integration
class TestFloodRCPIntegrationHandler:
    def test_integ_handler_address(
        self, geotiff_env_rcp, lambda_powertools_ctx, event_address_rcp
    ):
        got = handler(event=event_address_rcp, context=lambda_powertools_ctx)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_integ_handler_output(
        self, geotiff_env_rcp, lambda_powertools_ctx, event_address_rcp
    ):
        got = handler(event=event_address_rcp, context=lambda_powertools_ctx)

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

    def test_integ_handler_missing_geotiff_json(
        self, event_address_rcp, lambda_powertools_ctx
    ):
        got = handler(event=event_address_rcp, context=lambda_powertools_ctx)

        want_status_code = 500
        wanted_body = "Internal Server Error"

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_handler_lat_lon(
        self, geotiff_env_rcp, event_lat_lon_rcp, lambda_powertools_ctx
    ):
        got = handler(event=event_lat_lon_rcp, context=lambda_powertools_ctx)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_integ_handler_invalid_lat_lon(
        self, geotiff_env_rcp, event_invalid_lat_lon_rcp, lambda_powertools_ctx
    ):
        got = handler(event=event_invalid_lat_lon_rcp, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.MISSING_DATA

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_handler_conflict(
        self,
        geotiff_env_rcp,
        event_conflict_lat_lon_addr_rcp,
        lambda_powertools_ctx,
    ):
        got = handler(
            event=event_conflict_lat_lon_addr_rcp, context=lambda_powertools_ctx
        )

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR_RCP

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_invalid_address(
        self, geotiff_env_rcp, event_invalid_address_rcp, lambda_powertools_ctx
    ):
        got = handler(event=event_invalid_address_rcp, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.UNKNOWN_ADDRESS

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_oob_address(
        self, geotiff_env_rcp, event_oob_address_rcp, lambda_powertools_ctx
    ):
        got = handler(event=event_oob_address_rcp, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.OUT_OF_BOUNDS

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_invalid_year(
        self, geotiff_env_rcp, event_invalid_year, lambda_powertools_ctx
    ):
        got = handler(event=event_invalid_year, context=lambda_powertools_ctx)

        geotiff = json.loads(geotiff_env_rcp["GEOTIFF_JSON"])
        want_body = InvalidYearError(years=[entry["year"] for entry in geotiff]).msg
        want_status_code = StatusCodes.QUERYSTRING_ERROR[0]

        assert want_status_code == got["statusCode"]
        assert want_body == got["body"]

    #  2024-03-04: commented because google maps does not
    #   reply anymore with multiple addresses in this scenario
    # def test_integ_too_generic_address(
    #    self, geotiff_env_rcp, event_too_generic_address, lambda_powertools_ctx
    # ):
    #    got = handler(event=event_too_generic_address, context=lambda_powertools_ctx)
    #
    #    want_status_code, wanted_body = StatusCodes.UNKNOWN_ADDRESS
    #
    #    assert want_status_code == got["statusCode"]
    #    assert wanted_body == got["body"]
