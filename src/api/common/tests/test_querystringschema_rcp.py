import pytest
from common.input_schema import QueryStringRCPSchema, validate_query_params
from pydantic import BaseModel, ValidationError


@pytest.mark.unit
class TestQuerystringRCPSchema:
    def test_empty_schema(self):
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, {})

    def test_valid_schema(self):
        instance = {
            "address": "via verruca 1 trento",
            "year": "2030",
            "valid_years": [2030, 2050, 2070],
        }
        result = validate_query_params(QueryStringRCPSchema, instance)
        assert isinstance(result, BaseModel)
        assert isinstance(result.address, str)

    @pytest.mark.parametrize(
        "year,valid_years",
        [
            ("2040", [2030, 2050, 2070]),
            ("", [2030]),
            ("2030", []),
        ],
    )
    def test_invalid_years(self, year, valid_years):
        instance = {
            "address": "via verruca 1 trento",
            "year": year,
            "valid_years": valid_years,
        }
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)

    def test_missing_year(self):
        instance = {"address": "via verruca 1 trento", "valid_years": [2030, 2050]}
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)

    def test_invalid_address_lat_schema(self):
        instance = {"address": "via verruca 1 trento", "lat": "29"}
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)

    def test_invalid_address_lon_schema(self):
        instance = {"address": "via verruca 1 trento", "lon": "33"}
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)

    def test_invalid_address_lat_lon_schema(self):
        instance = {"address": "via verruca 1 trento", "lon": "33", "lat": "29"}
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)

    def test_invalid_lon_only(self):
        instance = {"lon": "33"}
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)

    def test_invalid_lat_only(self):
        instance = {"lat": "33"}
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)

    @pytest.mark.parametrize(
        "lat,lon",
        [
            ("27", "-22.0"),
            ("32", "45.0"),
            ("72.0", "44.9999"),
            ("32.125", "-0.5"),
            ("32.0005", "0.005"),
        ],
    )
    def test_valid_lat_lon_schema(self, lat, lon):
        instance = {"lon": lon, "lat": lat, "year": "2030", "valid_years": [2030, 2050]}
        result = validate_query_params(QueryStringRCPSchema, instance)
        assert isinstance(result, BaseModel)
        assert isinstance(result.lon, float)
        assert isinstance(result.lat, float)

    @pytest.mark.parametrize(
        "lat",
        [("93"), ("112"), ("1202"), ("73"), ("72.01")],
    )
    def test_lat_too_high(self, lat):
        instance = {"lon": "33", "lat": lat}
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)

    @pytest.mark.parametrize(
        "lat",
        [("26.9"), ("-3"), ("11")],
    )
    def test_lat_too_low(self, lat):
        instance = {"lon": "33", "lat": lat}
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)

    @pytest.mark.parametrize(
        "lon",
        [("-22.1"), ("-30.125"), ("-23.00")],
    )
    def test_lon_too_low(self, lon):
        instance = {"lon": lon, "lat": "27"}
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)

    @pytest.mark.parametrize(
        "lon",
        [("45.01"), ("45.0001"), ("90"), ("10000"), ("450")],
    )
    def test_lon_too_high(self, lon):
        instance = {"lon": lon, "lat": "27"}
        with pytest.raises(ValidationError):
            validate_query_params(QueryStringRCPSchema, instance)
