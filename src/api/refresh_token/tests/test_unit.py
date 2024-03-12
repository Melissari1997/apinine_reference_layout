import json

import pytest
import responses
from main import lambda_handler


@pytest.mark.unit
class TestRefreshTokenUnit:
    def test_handler_no_env(self):
        with pytest.raises(ValueError):
            lambda_handler({}, {})

    @responses.activate
    def test_handler(self, monkeypatch):
        url = "https://cognito-custom-domain.auth.eu-central-1.amazoncognito.com/oauth2/token"
        event_body = {"refresh_token": "my_refresh_token"}

        monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "INFO")
        monkeypatch.setenv("URL", url)
        monkeypatch.setenv("APP_CLIENT_ID", "abc12334")
        monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "REFRESH_TOKEN")

        want_body = {
            "id_token": "ey.id_token",
            "access_token": "ey.access_token",
            "expires_in": 3600,
            "token_type": "Bearer",
        }

        responses.add(
            responses.POST,
            url,
            json=want_body,
            status=200,
        )

        r = lambda_handler({"body": json.dumps(event_body)}, {})
        want = (200, want_body)
        assert want == (r["statusCode"], json.loads(r["body"]))
