import json

import pytest
from common.env_parser import BaselineEnvParser, RCPEnvParser
from common.errors import InvalidYearError


@pytest.mark.unit
class TestEnvironmentParser:
    def test_parse_missing_env_var(self):
        with pytest.raises(ValueError):
            BaselineEnvParser(environ={})

    def test_parse_malformed_env_var(self):
        environ = {"GEOTIFF_JSON": "{invalid json}"}
        with pytest.raises(ValueError):
            BaselineEnvParser(environ=environ)

    def test_parse_baseline_success(self, geotiff_baseline):
        environ = {"GEOTIFF_JSON": json.dumps(geotiff_baseline)}
        parser = BaselineEnvParser(environ=environ)
        filename_got = parser.get_filename()
        filename_want = geotiff_baseline[0]["path"]

        assert filename_got == filename_want

    @pytest.mark.parametrize("year", ["2030", "2040", "2050", 2030, 2040, 2050])
    def test_parse_rcp_success(self, geotiff_rcp, year):
        environ = {"GEOTIFF_JSON": json.dumps(geotiff_rcp)}
        parser = RCPEnvParser(environ=environ)
        want = [entry["path"] for entry in geotiff_rcp if entry["year"] == str(year)][0]
        got = parser.get_filename(year=year)

        assert got == want

    def test_parse_rcp_invalid_year(self, geotiff_rcp):
        environ = {"GEOTIFF_JSON": json.dumps(geotiff_rcp)}
        year = "1983"
        parser = RCPEnvParser(environ=environ)
        want_msg = InvalidYearError(
            valid_years=[entry["year"] for entry in geotiff_rcp]
        ).msg

        with pytest.raises(InvalidYearError) as excinfo:
            parser.get_filename(year=year)

        assert excinfo.value.msg == want_msg
