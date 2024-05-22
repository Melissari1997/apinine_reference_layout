import pytest
from common.status_codes import StatusCodes
from rcp import handler as handler_module


@pytest.mark.unit
class TestFloodUnit:
    def test_handler_address(
        self,
        geotiff_env_rcp,
        event_address_rcp,
        lambda_powertools_ctx,
        mockgeocoder,
        mockgeodatareaderflood,
        monkeypatch,
    ):
        monkeypatch.setattr(handler_module, "gmapsgeocoder", mockgeocoder)
        monkeypatch.setattr(handler_module, "riogeoreader", mockgeodatareaderflood)

        got = handler_module.handler(
            event=event_address_rcp, context=lambda_powertools_ctx
        )

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_handler_no_queryparams(
        self, geotiff_env_rcp, lambda_powertools_ctx, monkeypatch
    ):
        got = handler_module.handler(event={}, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR_RCP

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_handler_lat_lon(
        self,
        event_lat_lon_rcp,
        geotiff_env_rcp,
        lambda_powertools_ctx,
        mockgeocoder,
        mockgeodatareaderflood,
        monkeypatch,
    ):
        monkeypatch.setattr(handler_module, "gmapsgeocoder", mockgeocoder)
        monkeypatch.setattr(handler_module, "riogeoreader", mockgeodatareaderflood)

        got = handler_module.handler(
            event=event_lat_lon_rcp, context=lambda_powertools_ctx
        )

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    @pytest.mark.parametrize(
        "address,lat,lon,year",
        [
            ("addr", "27", "-22.0", "2040"),
            ("addr", "45.0", None, "2040"),
            ("addr", None, "44.9999", "2040"),
            (None, "32.125", None, "2040"),
            (None, None, "40", "2040"),
        ],
    )
    def test_handler_conflicting(
        self,
        address,
        lat,
        lon,
        year,
        geotiff_env_rcp,
        mockgeocoder,
        mockgeodatareaderflood,
        monkeypatch,
        lambda_powertools_ctx,
    ):
        monkeypatch.setattr(handler_module, "gmapsgeocoder", mockgeocoder)
        monkeypatch.setattr(handler_module, "riogeoreader", mockgeodatareaderflood)

        got = handler_module.handler(
            event={
                "queryStringParameters": {
                    "address": address,
                    "lon": lon,
                    "lat": lat,
                    "year": year,
                }
            },
            context=lambda_powertools_ctx,
        )

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR_RCP

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    @pytest.mark.parametrize(
        "lat,lon,year",
        [
            ("30", "72.0001", "2040"),
            ("26.9999", "30", "2040"),
            ("-54", "30", "2040"),
            ("30", "11123", "2040"),
            ("32323", "11123", "2040"),
        ],
    )
    def test_invalid_lat_lon(
        self,
        lat,
        lon,
        year,
        geotiff_env_rcp,
        lambda_powertools_ctx,
    ):
        got = handler_module.handler(
            event={"queryStringParameters": {"lon": lon, "lat": lat, "year": year}},
            context=lambda_powertools_ctx,
        )

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR_RCP

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_empty_address(
        self,
        geotiff_env_rcp,
        lambda_powertools_ctx,
    ):
        got = handler_module.handler(
            event={"queryStringParameters": {"address": ""}},
            context=lambda_powertools_ctx,
        )

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR_RCP

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]
