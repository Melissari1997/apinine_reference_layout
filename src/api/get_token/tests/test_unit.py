import json

import pytest
import responses
from main import lambda_handler


@pytest.mark.unit
class TestGetTokenUnit:
    def test_handler_no_env(self):
        with pytest.raises(ValueError):
            lambda_handler({}, {})

    # TODO: Parametrize  statusCode and body
    @responses.activate
    def test_handler(self, monkeypatch):
        url = "https://custom-cognito-domain.auth.eu-central-1.amazoncognito.com/oauth2/token"
        body = {"ok": 1}

        monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "INFO")
        monkeypatch.setenv("URL", url)
        monkeypatch.setenv("APP_CLIENT_ID", "abcd1234")
        monkeypatch.setenv("CALLBACK_URI", "https://example.com")
        monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "get_jwt_token")

        responses.add(
            responses.POST,
            url,
            json=body,
            status=200,
        )

        r = lambda_handler({}, {})
        want = (200, body)
        assert want == (r["statusCode"], json.loads(r["body"]))
