import main
import pytest
from common.status_codes import StatusCodes
from main import handler


@pytest.mark.unit
class TestFloodUnit:
    def test_handler_address(
        self,
        geotiff_path_s3,
        event_address,
        lambda_powertools_ctx,
        mockgeocoder,
        mockgeodatareaderflood,
        monkeypatch,
    ):
        monkeypatch.setattr(main, "gmapsgeocoder", mockgeocoder)
        monkeypatch.setattr(main, "riogeoreader", mockgeodatareaderflood)

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
        self,
        event_lat_lon,
        geotiff_path_s3,
        lambda_powertools_ctx,
        mockgeocoder,
        mockgeodatareaderflood,
        monkeypatch,
    ):
        monkeypatch.setattr(main, "gmapsgeocoder", mockgeocoder)
        monkeypatch.setattr(main, "riogeoreader", mockgeodatareaderflood)

        got = handler(event=event_lat_lon, context=lambda_powertools_ctx)

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
        address,
        lat,
        lon,
        geotiff_path_s3,
        mockgeocoder,
        mockgeodatareaderflood,
        monkeypatch,
        lambda_powertools_ctx,
    ):
        monkeypatch.setattr(main, "gmapsgeocoder", mockgeocoder)
        monkeypatch.setattr(main, "riogeoreader", mockgeodatareaderflood)

        got = handler(
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
        lat,
        lon,
        geotiff_path_s3,
        lambda_powertools_ctx,
    ):
        got = handler(
            event={"queryStringParameters": {"lon": lon, "lat": lat}},
            context=lambda_powertools_ctx,
        )

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
