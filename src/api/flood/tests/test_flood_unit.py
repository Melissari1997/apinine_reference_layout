import pytest
from geocoder.geocoder import Geocoder
from main import FloodKeys, main
from readgeodata.interfaces import GeoDataReader


class MockGeocoder(Geocoder):
    def __init__(self) -> None:
        pass

    def geocode(self, address: str) -> tuple[tuple[float, float], str]:
        return ((12.215283630441727, 44.88393348245498), "via verruca 1 trento")


class MockGeoDataReaderFlood(GeoDataReader):
    def sample_data_points(
        self,
        filename: str,
        coordinates: list[tuple],
        metadata: list[str],
        coordinates_crs: int = 4326,
    ):
        return {
            FloodKeys.WH_20: [0.0],
            FloodKeys.WH_100: [0.01],
            FloodKeys.WH_200: [0.3],
            FloodKeys.VULN_20: [0.0],
            FloodKeys.VULN_100: [0.0001],
            FloodKeys.VULN_200: [0.56],
            FloodKeys.RISK_INDEX: [2],
            FloodKeys.AAL: [0.032],
            "metadata": {FloodKeys.NATIONAL_AAL: 0.0423},
        }


@pytest.mark.unit
class TestFloodUnit:
    def test_flood_with_lat_lon(self):
        lon, lat = 12.215283630441727, 44.88393348245498
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderFlood()
        got = main(
            filename="random_filename",
            address=None,
            lon=lon,
            lat=lat,
            geocoder=gmaps,
            geodatareader=rioreader,
        )

        # Checking only format and types, not the values
        assert isinstance(got, dict)

    def test_with_address(self):
        lon, lat = (None, None)
        gmaps = MockGeocoder()
        rioreader = MockGeoDataReaderFlood()
        address = "via verruca 1 trento"

        want = {
            "address": "via verruca 1 trento",
            "lat": 44.88393348245498,
            "lon": 12.215283630441727,
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
            "average_annual_loss": {"value": 0.032, "national_average": 0.0423},
        }

        got = main(
            filename="random_filename",
            address=address,
            lon=lon,
            lat=lat,
            geocoder=gmaps,
            geodatareader=rioreader,
        )

        assert want == got
