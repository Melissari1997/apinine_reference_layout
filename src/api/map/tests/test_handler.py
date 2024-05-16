from flood.handler import handler


class TestHandler:
    def test_handler(self, geotiff_path_s3, lambda_powertools_ctx):
        response = handler(
            event={
                "queryStringParameters": {
                    "lat": "44.379260542097036",
                    "lon": "9.069138608016194",
                    "layer": "aal",
                }
            },
            context=lambda_powertools_ctx,
        )

        assert isinstance(response, dict)
