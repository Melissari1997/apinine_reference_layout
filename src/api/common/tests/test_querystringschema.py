import pytest
from common.input_schema import validate_query_params
from pydantic import ValidationError


class TestQuerystringSchema:
    def test_empty_schema(self):
        with pytest.raises(ValidationError):
            validate_query_params({})

    def test_valid_address_schema(self):
        instance = {"address": "via verruca 1 trento"}
        result = validate_query_params(instance)
        assert isinstance(result, dict)
        assert isinstance(result["address"], str)

    def test_invalid_address_lat_schema(self):
        instance = {"address": "via verruca 1 trento", "lat": "29"}
        with pytest.raises(ValidationError):
            validate_query_params(instance)

    def test_invalid_address_lon_schema(self):
        instance = {"address": "via verruca 1 trento", "lon": "33"}
        with pytest.raises(ValidationError):
            validate_query_params(instance)

    def test_invalid_address_lat_lon_schema(self):
        instance = {"address": "via verruca 1 trento", "lon": "33", "lat": "29"}
        with pytest.raises(ValidationError):
            validate_query_params(instance)

    def test_invalid_lon_only(self):
        instance = {"lon": "33"}
        with pytest.raises(ValidationError):
            validate_query_params(instance)

    def test_invalid_lat_only(self):
        instance = {"lat": "33"}
        with pytest.raises(ValidationError):
            validate_query_params(instance)

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
        instance = {"lon": lon, "lat": lat}
        result = validate_query_params(instance)
        assert isinstance(result, dict)
        assert isinstance(result["lon"], float)
        assert isinstance(result["lat"], float)

    @pytest.mark.parametrize(
        "lat",
        [("93"), ("112"), ("1202"), ("73"), ("72.01")],
    )
    def test_lat_too_high(self, lat):
        instance = {"lon": "33", "lat": lat}
        with pytest.raises(ValidationError):
            validate_query_params(instance)

    @pytest.mark.parametrize(
        "lat",
        [("26.9"), ("-3"), ("11")],
    )
    def test_lat_too_low(self, lat):
        instance = {"lon": "33", "lat": lat}
        with pytest.raises(ValidationError):
            validate_query_params(instance)

    @pytest.mark.parametrize(
        "lon",
        [("-22.1"), ("-30.125"), ("-23.00")],
    )
    def test_lon_too_low(self, lon):
        instance = {"lon": lon, "lat": "27"}
        with pytest.raises(ValidationError):
            validate_query_params(instance)

    @pytest.mark.parametrize(
        "lon",
        [("45.01"), ("45.0001"), ("90"), ("10000"), ("450")],
    )
    def test_lon_too_high(self, lon):
        instance = {"lon": lon, "lat": "27"}
        with pytest.raises(ValidationError):
            validate_query_params(instance)
