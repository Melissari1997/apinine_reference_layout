import pytest
from main import handler


@pytest.mark.integration
class TestWildfireIntegration:
    def test_integ_handler_address(
        self, geotiff_path_s3, lambda_powertools_ctx, event_address
    ):
        got = handler(event=event_address, context=lambda_powertools_ctx)

        want_status_code = 200

        assert want_status_code == got["statusCode"]

    def test_integ_handler_lat_lon(
        self, geotiff_path_s3, lambda_powertools_ctx, event_lat_lon
    ):
        got = handler(event=event_lat_lon, context=lambda_powertools_ctx)

        want_status_code = 200

        assert want_status_code == got["statusCode"]
