import pytest
from main import lambda_handler


@pytest.mark.unit
class TestGetLoginUnit:
    def test_handler_no_env(self):
        with pytest.raises(ValueError):
            lambda_handler({}, {})

    def test_handler(self, monkeypatch):
        url = "https://custom-cognito-domain.auth.eu-central-1.amazoncognito.com/oauth2/login"

        monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "INFO")
        monkeypatch.setenv("URL", url)
        monkeypatch.setenv("APP_CLIENT_ID", "abcd1234")
        monkeypatch.setenv("CALLBACK_URI", "https://example.com")
        monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "LOGIN")

        want = {
            "statusCode": "302",
            "headers": {
                "Location": "https://custom-cognito-domain.auth.eu-central-1.amazoncognito.com/oauth2/login?response_type:code&client_id=abcd1234&scope=email+openid&redirect_uri=https%3A%2F%2Fexample.com"
            },
        }

        r = lambda_handler({}, {})
        assert want == r
