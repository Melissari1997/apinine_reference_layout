import pytest
from readgeodata.rasterioreader import RasterIOReader
from common.schema import NOT_IMPLEMENTED_PLACEHOLDER
from main import main


@pytest.mark.unit
class TestFloodUnit:
    def test_flood_with_lat_lon(self, mockgeocoder):
        riogeoreader = RasterIOReader()
        coordinates = [(12.286326, 41.725469, None), (12.285276, 41.726315, None)]
        got = main(
            filename="tests/fixtures/ostia_near_sea_fixture_1b.tiff",
            tiff_metadata=[],
            coordinates=coordinates,
            geocoder=mockgeocoder,
            geodatareader=riogeoreader,
        )

        # Checking only format and types, not the values
        assert isinstance(got, dict)
