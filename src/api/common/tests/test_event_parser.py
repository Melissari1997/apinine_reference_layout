import json

import pytest
from common.event_parser import (
    parse_aws_event,
)
from common.input_schema import RiskInputSchema, RiskRCPInputSchema
from common.parse_env import BaselineEnvParser, RCPEnvParser
from common.status_codes import StatusCodes
from pydantic import ValidationError


@pytest.mark.unit
class TestParseAwsEvent:
    def test_parse_empty_event(self):
        event = {}
        with pytest.raises(ValueError):
            parse_aws_event(event=event, env_parser={}, model=RiskInputSchema)

    def test_parse_aws_event_baseline_success(
        self, geotiff_json_baseline, event_address
    ):
        filename_want = json.loads(geotiff_json_baseline)[0]["path"]
        address_want = event_address["queryStringParameters"]["address"]
        envparser = BaselineEnvParser(environ={"GEOTIFF_JSON": geotiff_json_baseline})
        filename, model = parse_aws_event(
            event=event_address, env_parser=envparser, model=RiskInputSchema
        )
        address = model.address
        lat = model.lat
        lon = model.lon

        assert filename == filename_want
        assert address == address_want
        assert lat is None
        assert lon is None

    def test_parse_aws_event_rcp_success(
        self, geotiff_json_rcp, event_address_rcp, monkeypatch
    ):
        year = event_address_rcp["queryStringParameters"]["year"]
        filename_want = [
            entry["path"]
            for entry in json.loads(geotiff_json_rcp)
            if entry["year"] == str(year)
        ][0]
        address_want = event_address_rcp["queryStringParameters"]["address"]
        envparser = RCPEnvParser(environ={"GEOTIFF_JSON": geotiff_json_rcp})
        filename, model = parse_aws_event(
            event=event_address_rcp, env_parser=envparser, model=RiskRCPInputSchema
        )
        address = model.address
        lat = model.lat
        lon = model.lon

        assert filename == filename_want
        assert address == address_want
        assert lat is None
        assert lon is None

    def test_parse_aws_event_baseline_returns_400_on_empty_querystringparameters(
        self, geotiff_json_baseline, monkeypatch
    ):
        # When no query parameters are supplied, AWS sets "queryStringParameters" to None
        event = {"queryStringParameters": None}
        monkeypatch.setenv("GEOTIFF_JSON", geotiff_json_baseline)
        envparser = BaselineEnvParser(environ={"GEOTIFF_JSON": geotiff_json_baseline})
        with pytest.raises(ValidationError) as excinfo:
            parse_aws_event(event=event, env_parser=envparser, model=RiskInputSchema)

        want_code, want_msg = StatusCodes.QUERYSTRING_ERROR
        assert excinfo.value.title == want_msg

    def test_parse_aws_event_rcp_returns_400_on_empty_querystringparameters(
        self, geotiff_json_rcp, monkeypatch
    ):
        # When no query parameters are supplied, AWS sets "queryStringParameters" to None
        event = {"queryStringParameters": None}
        monkeypatch.setenv("GEOTIFF_JSON", geotiff_json_rcp)
        envparser = RCPEnvParser(environ={"GEOTIFF_JSON": geotiff_json_rcp})
        with pytest.raises(ValidationError) as excinfo:
            parse_aws_event(event=event, env_parser=envparser, model=RiskRCPInputSchema)

        want_code, want_msg = StatusCodes.QUERYSTRING_ERROR_RCP
        assert excinfo.value.title == want_msg
