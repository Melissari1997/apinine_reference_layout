import json

import boto3
import pytest
import responses
from main import get_user_email, get_userinfo_from_db, lambda_handler
from moto import mock_aws


@pytest.mark.unit
class TestGetUserUnit:
    @responses.activate
    def test_get_user_email(self):
        userinfo_endpoint = "http://website.com"
        want_email = "myemail@email.com"
        want_body = {"email": want_email}

        responses.add(
            responses.GET,
            userinfo_endpoint,
            json=want_body,
            status=200,
        )
        assert get_user_email(userinfo_endpoint, {}) == want_email

    @responses.activate
    def test_get_userinfo_from_db(self):
        userinfo_endpoint = "http://website.com"
        want_body = {}
        want_status_code = 404
        responses.add(
            responses.GET,
            userinfo_endpoint,
            json=want_body,
            status=want_status_code,
        )
        access_token = ""
        result = get_userinfo_from_db(
            userinfo_endpoint=userinfo_endpoint, access_token=access_token, db=None
        )

        assert isinstance(result, tuple)
        assert result[0] == 404
        assert result[1] == {}

    @mock_aws
    def test_handler(self, monkeypatch):
        url = "http://myurl.com"
        event_body = {"headers": {"Authorization": "Bearer my_access_token"}}
        my_parameter = "myparam"
        email = "email@email.com"
        want = {"name": "username", "email": email}
        db = [want]

        monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "INFO")
        monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "REFRESH_TOKEN")
        monkeypatch.setenv("URL_USERINFO", url)
        monkeypatch.setenv("USER_DB_PARAMETER_NAME", my_parameter)

        client = boto3.client("ssm", region_name="eu-central-1")
        client.put_parameter(Name=my_parameter, Value=json.dumps(db), Type="String")

        responses.add(
            responses.GET,
            url,
            json={"email": email},
            status=200,
        )

        r = lambda_handler(event_body, context=None)
        want = (200, want)
        assert want == (r["statusCode"], json.loads(r["body"]))

    @mock_aws
    def test_handler_user_not_found(self, monkeypatch):
        url = "http://myurl.com"
        event_body = {"headers": {"Authorization": "Bearer my_access_token"}}
        my_parameter = "myparam"
        email = "email@email.com"
        db = []

        monkeypatch.setenv("POWERTOOLS_LOG_LEVEL", "INFO")
        monkeypatch.setenv("POWERTOOLS_SERVICE_NAME", "REFRESH_TOKEN")
        monkeypatch.setenv("URL_USERINFO", url)
        monkeypatch.setenv("USER_DB_PARAMETER_NAME", my_parameter)

        client = boto3.client("ssm", region_name="eu-central-1")
        client.put_parameter(Name=my_parameter, Value=json.dumps(db), Type="String")

        responses.add(
            responses.GET,
            url,
            json={"email": email},
            status=200,
        )

        r = lambda_handler(event_body, context=None)
        want = (404, {})
        assert want == (r["statusCode"], json.loads(r["body"]))
