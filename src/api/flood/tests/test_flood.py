from main import main


class TestFlood:
    def test_flood_with_address(self):
        # lon, lat = 9.081023090011794, 44.395733386344574
        lon, lat = 12.215283630441727, 44.88393348245498
        got = main(lon=lon, lat=lat)
        want = {
            "address": None,
            "flood_risk_assessment": {
                "return_period_20y": {
                    "intensity": {"water_height": 0.0},
                    "vulnerability": 0.0,
                },
                "return_period_100y": {
                    "intensity": {"water_height": 0.0},
                    "vulnerability": 0.0,
                },
                "return_period_200y": {
                    "intensity": {"water_height": 0.9967429},
                    "vulnerability": 0.55,
                },
            },
            "risk_index": 1.0,
            "average_annual_loss": 0.004125,
            "national_average_annual_loss": 0.0423,
        }
        assert got == want
