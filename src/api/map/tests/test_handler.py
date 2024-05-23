import json

import pytest
from common.status_codes import StatusCodes
from drought.baseline.handler import handler as drought_baseline_handler
from flood.baseline.handler import handler as flood_baseline_handler
from wildfire.baseline.handler import handler as wildfire_baseline_handler


@pytest.mark.integration
class TestHandlerFlood:
    def test_handler(self, flood_baseline_geotiff_json, lambda_powertools_ctx):
        response = flood_baseline_handler(
            event={
                "queryStringParameters": {
                    "lat": "44.379260542097036",
                    "lon": "9.069138608016194",
                    "layer": "aal",
                }
            },
            context=lambda_powertools_ctx,
        )

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["type"] == "FeatureCollection"
        assert "metadata" in body
        assert "features" in body

    def test_handler_wrong_layer(
        self, flood_baseline_geotiff_json, lambda_powertools_ctx
    ):
        response = flood_baseline_handler(
            event={
                "queryStringParameters": {
                    "lat": "44.379260542097036",
                    "lon": "9.069138608016194",
                    "layer": "wrong",
                }
            },
            context=lambda_powertools_ctx,
        )

        want_status_code, want_err_message = StatusCodes.LAYER_NOT_FOUND
        assert response["statusCode"] == want_status_code
        assert response["body"] == want_err_message


@pytest.mark.integration
class TestHandlerWildfire:
    def test_handler(self, wildfire_baseline_geotiff_json, lambda_powertools_ctx):
        response = wildfire_baseline_handler(
            event={
                "queryStringParameters": {
                    "lat": "44.379260542097036",
                    "lon": "9.069138608016194",
                    "layer": "wildfire rp 10 layer, band 2",
                }
            },
            context=lambda_powertools_ctx,
        )

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["type"] == "FeatureCollection"
        assert "metadata" in body
        assert "features" in body


@pytest.mark.integration
class TestHandlerDrought:
    def test_handler(self, drought_baseline_geotiff_json, lambda_powertools_ctx):
        response = drought_baseline_handler(
            event={
                "queryStringParameters": {
                    "lat": "44.379260542097036",
                    "lon": "9.069138608016194",
                    "layer": "duration_rp20y",
                }
            },
            context=lambda_powertools_ctx,
        )

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["type"] == "FeatureCollection"
        assert "metadata" in body
        assert "features" in body
