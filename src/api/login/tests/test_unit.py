import pytest
from main import lambda_handler


@pytest.mark.unit
class TestGetLoginUnit:
    def test_handler_no_env(self):
        with pytest.raises(ValueError):
            lambda_handler({}, {})

    @pytest.mark.parametrize(
        "event",
        [{}, {"queryStringParameters": None}],
    )
    def test_handler(self, event, monkeypatch):
        url = "https://custom-cognito-domain.auth.eu-central-1.amazoncognito.com/login"

        monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "INFO")
        monkeypatch.setenv("URL", url)
        monkeypatch.setenv("APP_CLIENT_ID", "abcd1234")
        monkeypatch.setenv("CALLBACK_URI", "https://example.com")
        monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "LOGIN")

        want = {
            "statusCode": "302",
            "headers": {
                "Location": "https://custom-cognito-domain.auth.eu-central-1.amazoncognito.com/login?response_type=code&client_id=abcd1234&scope=email+openid&redirect_uri=https%3A%2F%2Fexample.com"
            },
        }

        r = lambda_handler(event, {})
        assert want == r

    def test_handler_with_callback_uri(self, monkeypatch):
        url = "https://custom-cognito-domain.auth.eu-central-1.amazoncognito.com/login"

        monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "INFO")
        monkeypatch.setenv("URL", url)
        monkeypatch.setenv("APP_CLIENT_ID", "abcd1234")
        monkeypatch.setenv("CALLBACK_URI", "https://example.com")
        monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "LOGIN")

        want = {
            "statusCode": "302",
            "headers": {
                "Location": "https://custom-cognito-domain.auth.eu-central-1.amazoncognito.com/login?response_type=code&client_id=abcd1234&scope=email+openid&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Flogin"
            },
        }

        callback_uri = "http://localhost:3000/login"
        r = lambda_handler(
            event={"queryStringParameters": {"callback_uri": callback_uri}}, context={}
        )
        assert want == r
