import json

import pytest
from baseline.handler import handler


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

    def test_integ_handler_output(
        self, geotiff_path_s3, lambda_powertools_ctx, event_lat_lon
    ):
        got = handler(event=event_lat_lon, context=lambda_powertools_ctx)

        keys_want = {
            "address",
            "lat",
            "lon",
            "land_use",
            "wildfire_risk_assessment",
            "risk_index",
            "average_annual_loss",
            "hazard_index",
        }

        body = json.loads(got["body"])

        assert set(body) == keys_want
        assert isinstance(
            body["wildfire_risk_assessment"]["return_period_2y"]["vulnerability"], float
        )
