import pytest
from common.schema import NOT_IMPLEMENTED_PLACEHOLDER
from main import main


@pytest.mark.unit
class TestFloodUnit:
    def test_flood_with_lat_lon(self, mockgeocoder, mockgeodatareaderflood):
        lon, lat = 12.215283630441727, 44.88393348245498
        got = main(
            filename="random_filename",
            address=None,
            lon=lon,
            lat=lat,
            geocoder=mockgeocoder,
            geodatareader=mockgeodatareaderflood,
        )

        # Checking only format and types, not the values
        assert isinstance(got, dict)

    def test_with_address(self, mockgeocoder, mockgeodatareaderflood):
        lon, lat = (None, None)
        address = "via verruca 1 trento"

        want = {
            "address": "via verruca 1 trento",
            "lat": 44.88393348245498,
            "lon": 12.215283630441727,
            "land_use": "Residential",
            "flood_risk_assessment": {
                "return_period_20y": {
                    "intensity": {"water_height": 0.0},
                    "vulnerability": 0.0,
                },
                "return_period_100y": {
                    "intensity": {"water_height": 0.01},
                    "vulnerability": 0.0001,
                },
                "return_period_200y": {
                    "intensity": {"water_height": 0.3},
                    "vulnerability": 0.56,
                },
            },
            "risk_index": 2,
            "hazard_index": NOT_IMPLEMENTED_PLACEHOLDER,
            "average_annual_loss": {
                "value": 0.032,
                "national_average": 0.0034,
                "regional_average": NOT_IMPLEMENTED_PLACEHOLDER,
            },
        }

        got = main(
            filename="random_filename",
            address=address,
            lon=lon,
            lat=lat,
            geocoder=mockgeocoder,
            geodatareader=mockgeodatareaderflood,
        )

        assert want == got
