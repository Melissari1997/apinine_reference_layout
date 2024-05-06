import json

import pytest
from common.errors import QuerystringInputError
from common.event_parser import (
    BaselineParser,
    RCPParser,
    is_baseline_scenario,
    parse_aws_event,
)
from common.status_codes import StatusCodes


class TestParseAwsEvent:
    def test_parse_missing_env_var(self):
        event = {}
        with pytest.raises(ValueError):
            parse_aws_event(event=event)

    def test_parse_malformed_env_var(self, monkeypatch):
        event = {}
        monkeypatch.setenv("GEOTIFF_JSON", "{invalid json}")
        with pytest.raises(ValueError):
            parse_aws_event(event=event)

    def test_is_baseline_scenario_true(self, geotiff_baseline):
        assert is_baseline_scenario(geotiff_baseline)

    def test_is_baseline_scenario_rcp(self, geotiff_baseline):
        geotiff_list = [
            {
                "climate_scenario": "rcp45",
                "year": "2030",
                "path": "my-s3-path-rcp45-2030.tif",
            },
            {
                "climate_scenario": "rcp45",
                "year": "2040",
                "path": "my-s3-path-rcp26-2040.tif",
            },
        ]
        want = False
        assert is_baseline_scenario(geotiff_list) is want

    def test_is_baseline_scenario_malformed_rcp_multiple_scenarios(
        self, geotiff_baseline
    ):
        geotiff_list = [
            {
                "climate_scenario": "rcp45",
                "year": "2030",
                "path": "my-s3-path-rcp45-2030.tif",
            },
            {
                "climate_scenario": "rcp26",
                "year": "2040",
                "path": "my-s3-path-rcp26-2040.tif",
            },
        ]
        with pytest.raises(ValueError):
            is_baseline_scenario(geotiff_list)

    def test_is_baseline_scenario_malformed_rcp_repeated_year(self, geotiff_baseline):
        geotiff_list = [
            {
                "climate_scenario": "rcp45",
                "year": "2030",
                "path": "my-s3-path-rcp45-2030.tif",
            },
            {
                "climate_scenario": "rcp45",
                "year": "2030",
                "path": "my-s3-path-2-rcp45-2030.tif",
            },
        ]
        with pytest.raises(ValueError):
            is_baseline_scenario(geotiff_list)

    def test_parse_aws_event_baseline_success(self, geotiff_json_baseline, monkeypatch):
        address_want = "via verruca 1 trento"
        filename_want = json.loads(geotiff_json_baseline)[0]["path"]
        event = {"queryStringParameters": {"address": address_want}}
        monkeypatch.setenv("GEOTIFF_JSON", geotiff_json_baseline)
        filename, address, lat, lon = parse_aws_event(event=event)

        assert filename == filename_want
        assert address == address_want
        assert lat is None
        assert lon is None

    def test_parse_aws_event_rcp_success(self, geotiff_json_rcp, monkeypatch):
        year = "2050"
        address_want = "via verruca 1 trento"
        filename_want = [
            entry["path"]
            for entry in json.loads(geotiff_json_rcp)
            if entry["year"] == year
        ][0]
        event = {"queryStringParameters": {"address": address_want, "year": year}}
        monkeypatch.setenv("GEOTIFF_JSON", geotiff_json_rcp)
        filename, address, lat, lon = parse_aws_event(event=event)

        assert filename == filename_want
        assert address == address_want
        assert lat is None
        assert lon is None


class TestBaselineParser:
    def test_parse_address_ok(self, geotiff_baseline, monkeypatch):
        address_want = "via verruca 1 trento"
        event = {"queryStringParameters": {"address": address_want}}
        filename_want = geotiff_baseline[0]["path"]

        filename, address, lat, lon = BaselineParser(geotiff_baseline).parse(
            event=event
        )
        assert filename == filename_want
        assert address == address_want
        assert lat is None
        assert lon is None

    def test_parse_lat_lon_ok(self, geotiff_baseline, monkeypatch):
        lat_want = "46"
        lon_want = "11"
        event = {"queryStringParameters": {"lat": lat_want, "lon": lon_want}}
        filename_want = geotiff_baseline[0]["path"]

        filename, address, lat, lon = BaselineParser(geotiff_baseline).parse(
            event=event
        )
        assert filename == filename_want
        assert lat == float(lat_want)
        assert lon == float(lon_want)

    @pytest.mark.parametrize(
        "address,lat,lon",
        [
            ("via verruca 1, trento", "46", "11"),
            ("via verruca 1, trento", "46", None),
            ("via verruca 1, trento", None, "11"),
            (None, "46", None),
            (None, None, None),
        ],
    )
    def test_parse_invalid_event(
        self, address, lat, lon, geotiff_baseline, monkeypatch
    ):
        event = {"queryStringParameters": {}}
        if address:
            event["queryStringParameters"]["address"] = address

        if lat:
            event["queryStringParameters"]["lat"] = lat

        if lon:
            event["queryStringParameters"]["lon"] = lon

        with pytest.raises(QuerystringInputError) as excinfo:
            BaselineParser(geotiff_baseline).parse(event=event)

        want_code, want_msg = StatusCodes.QUERYSTRING_ERROR
        assert excinfo.value.code == want_code
        assert excinfo.value.msg == want_msg


class TestRCPParser:

    @pytest.mark.parametrize(
        "year",
        ["2030", "2040", "2050"],
    )
    def test_parse_valid_year(self, year, geotiff_rcp, monkeypatch):
        want_filename = [
            entry["path"] for entry in geotiff_rcp if entry["year"] == year
        ][0]
        want_address = "via verruca 1 trento"

        event = {"queryStringParameters": {"address": want_address, "year": year}}

        got_filename, got_address, got_lat, got_lon = RCPParser(geotiff_rcp).parse(
            event=event
        )
        assert got_filename == want_filename
        assert got_address == want_address
        assert got_lat is None
        assert got_lon is None

    def test_parse_year_not_in_query_params(self, geotiff_rcp, monkeypatch):
        event = {"queryStringParameters": {"address": "via verruca 1 trento"}}
        parser = RCPParser(geotiff_rcp)
        with pytest.raises(QuerystringInputError) as excinfo:
            parser.parse(event=event)

        want_code, want_msg = StatusCodes.QUERYSTRING_ERROR_RCP
        want_msg = want_msg.format(parser.years)
        assert excinfo.value.code == want_code
        assert excinfo.value.msg == want_msg

    def test_parse_empty_year(self, geotiff_rcp, monkeypatch):
        event = {
            "queryStringParameters": {"address": "via verruca 1 trento", "year": ""}
        }
        parser = RCPParser(geotiff_rcp)
        with pytest.raises(QuerystringInputError) as excinfo:
            parser.parse(event=event)

        want_code, want_msg = StatusCodes.QUERYSTRING_ERROR_RCP
        want_msg = want_msg.format(parser.years)
        assert excinfo.value.code == want_code
        assert excinfo.value.msg == want_msg
