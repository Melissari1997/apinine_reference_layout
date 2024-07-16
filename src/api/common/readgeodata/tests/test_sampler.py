import pytest
from readgeodata.rasterioreader import RasterIOReader
from readgeodata.sampler import sample


@pytest.mark.unit
class TestSampleFlood:
    def test_flood_with_lat_lon(self, mockgeocoder):
        riogeoreader = RasterIOReader()
        coordinates = [(12.286326, 41.725469, None), (12.285276, 41.726315, None)]
        got = sample(
            filename="src/api/common/readgeodata/tests/fixtures/ostia_near_sea_fixture_1b.tiff",
            tiff_metadata=[],
            coordinates=coordinates,
            geocoder=mockgeocoder,
            geodatareader=riogeoreader,
        )

        # Checking only format and types, not the values
        assert isinstance(got, dict)
