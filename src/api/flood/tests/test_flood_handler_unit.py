import pytest
from baseline import handler as baseline_handler
from common.status_codes import StatusCodes
from rcp import handler as rcp_handler


@pytest.mark.parametrize(
    "handler_module",
    [baseline_handler, rcp_handler],
)
@pytest.mark.unit
class TestFloodUnit:
    def test_handler_address(
        self,
        handler_module,
        geotiff_path_s3,
        event_address,
        lambda_powertools_ctx,
        mockgeocoder,
        mockgeodatareaderflood,
        monkeypatch,
    ):
        monkeypatch.setattr(handler_module, "gmapsgeocoder", mockgeocoder)
        monkeypatch.setattr(handler_module, "riogeoreader", mockgeodatareaderflood)

        got = handler_module.handler(event=event_address, context=lambda_powertools_ctx)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_handler_no_queryparams(
        self, handler_module, geotiff_path_s3, lambda_powertools_ctx, monkeypatch
    ):
        got = handler_module.handler(event={}, context=lambda_powertools_ctx)

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_handler_lat_lon(
        self,
        handler_module,
        event_lat_lon,
        geotiff_path_s3,
        lambda_powertools_ctx,
        mockgeocoder,
        mockgeodatareaderflood,
        monkeypatch,
    ):
        monkeypatch.setattr(handler_module, "gmapsgeocoder", mockgeocoder)
        monkeypatch.setattr(handler_module, "riogeoreader", mockgeodatareaderflood)

        got = handler_module.handler(event=event_lat_lon, context=lambda_powertools_ctx)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    @pytest.mark.parametrize(
        "address,lat,lon",
        [
            ("addr", "27", "-22.0"),
            ("addr", "45.0", None),
            ("addr", None, "44.9999"),
            (None, "32.125", None),
            (None, None, "40"),
        ],
    )
    def test_handler_conflicting(
        self,
        handler_module,
        address,
        lat,
        lon,
        geotiff_path_s3,
        mockgeocoder,
        mockgeodatareaderflood,
        monkeypatch,
        lambda_powertools_ctx,
    ):
        monkeypatch.setattr(handler_module, "gmapsgeocoder", mockgeocoder)
        monkeypatch.setattr(handler_module, "riogeoreader", mockgeodatareaderflood)

        got = handler_module.handler(
            event={
                "queryStringParameters": {"address": address, "lon": lon, "lat": lat}
            },
            context=lambda_powertools_ctx,
        )

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    @pytest.mark.parametrize(
        "lat,lon",
        [
            ("30", "72.0001"),
            ("26.9999", "30"),
            ("-54", "30"),
            ("30", "11123"),
            ("32323", "11123"),
        ],
    )
    def test_invalid_lat_lon(
        self,
        handler_module,
        lat,
        lon,
        geotiff_path_s3,
        lambda_powertools_ctx,
    ):
        got = handler_module.handler(
            event={"queryStringParameters": {"lon": lon, "lat": lat}},
            context=lambda_powertools_ctx,
        )

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_empty_address(
        self,
        handler_module,
        geotiff_path_s3,
        lambda_powertools_ctx,
    ):
        got = handler_module.handler(
            event={"queryStringParameters": {"address": ""}},
            context=lambda_powertools_ctx,
        )

        want_status_code, wanted_body = StatusCodes.QUERYSTRING_ERROR

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]
