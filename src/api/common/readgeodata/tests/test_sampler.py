from geocoder.gmaps_geocoder import GMapsGeocoder
import pytest
from readgeodata.rasterioreader import RasterIOReader
from readgeodata.sampler import sample
import numpy as np


@pytest.mark.unit
class TestSampleFlood:
    def compare_outputs(self, want: dict, got: dict) -> bool:
        """
        Compare two dictionaries recursively to check if they are almost equal.

        Args:
            want (dict): The expected dictionary.
            got (dict): The actual dictionary.
        """
        assert got.keys() == want.keys()

        for k, v in got.items():
            if isinstance(v, dict):
                self.compare_outputs(want[k], v)
            elif v is None or want[k] is None:
                assert v == want[k]
            elif isinstance(v, str):
                assert str(v) == str(want[k])
            elif isinstance(v, list):
                assert len(v) == len(want[k])
                for item_got, item_want in zip(v, want[k]):
                    if isinstance(item_got, (float, int)):
                        np.testing.assert_almost_equal(
                            actual=item_got, desired=item_want, decimal=5
                        )
                    else:
                        assert item_got == item_want
            else:
                np.testing.assert_almost_equal(actual=v, desired=want[k], decimal=5)

    def test_flood_with_lat_lon(self, mockgeocoder):
        riogeoreader = RasterIOReader()
        coordinates = [(12.286326, 41.725469, None), (12.285276, 41.726315, None)]
        got = sample(
            filename="src/api/common/readgeodata/tests/fixtures/ostia_near_sea_fixture_1b.tiff",
            coordinates=coordinates,
            geodatareader=riogeoreader,
        )

        # Checking only format and types, not the values
        assert isinstance(got, dict)

    def test_flood_with_address(self, monkeypatch):
        riogeoreader = RasterIOReader()
        geocoder = GMapsGeocoder()
        valid_address1 = "Not existing"
        valid_address2 = "Lungomare Paolo Toscanelli, 63, 00122 Lido di Ostia RM"

        monkeypatch.setenv("GMAPS_SECRET_NAME", "apinine/gmaps_apikey")
        monkeypatch.setenv("GMAPS_SECRET_REGION", "eu-central-1")

        coordinates = [(None, None, valid_address1), (None, None, valid_address2)]
        got = sample(
            filename="src/api/common/readgeodata/tests/fixtures/ostia_near_sea_fixture_1b.tiff",
            coordinates=coordinates,
            geodatareader=riogeoreader,
        )

        # Checking only format and types, not the values
        assert isinstance(got, dict)

    @pytest.mark.parametrize(
        "coordinates, want",
        [
            (
                [(41.51808, 11.81210, None), (42.33055, 11.24322, None)],
                {
                    "band1": [-2.0, -2.0],
                    "metadata": {},
                    "latitude": [41.51808, 42.33055],
                    "longitude": [11.81210, 11.24322],
                    "addresses": [None, None],
                    "recognized_latitude": [41.51808, 42.33055],
                    "recognized_longitude": [11.81210, 11.24322],
                    "recognized_address": [None, None],
                    "message": [None, None],
                },
            ),
            (
                [(41.725469, 12.286326, None), (41.726315, 12.285276, None)],
                {
                    "band1": [-2.0, 0.02111816],
                    "metadata": {},
                    "latitude": [41.725469, 41.726315],
                    "longitude": [12.286326, 12.285276],
                    "addresses": [None, None],
                    "recognized_latitude": [41.725469, 41.726315],
                    "recognized_longitude": [12.286326, 12.285276],
                    "recognized_address": [None, None],
                    "message": [None, None],
                },
            ),  # first in water, second on land
        ],
    )
    def test_sample_on_land_and_water(self, coordinates, want):
        gmapsgeocoder = GMapsGeocoder()
        riogeoreader = RasterIOReader()
        got = sample(
            filename="src/api/common/readgeodata/tests/fixtures/ostia_near_sea_fixture_1b.tiff",
            coordinates=coordinates,
            geocoder=gmapsgeocoder,
            geodatareader=riogeoreader,
        )

        self.compare_outputs(want=want, got=got)

    @pytest.mark.parametrize(
        "coordinates,want",
        [
            (
                [(41.51808, 11.81210, None), (42.33055, 11.24322, None)],
                {
                    "band1": [-2.0, -2.0],
                    "band2": [-2.0, -2.0],
                    "band3": [-2.0, -2.0],
                    "latitude": [41.51808, 42.33055],
                    "longitude": [11.81210, 11.24322],
                    "addresses": [None, None],
                    "recognized_latitude": [41.51808, 42.33055],
                    "recognized_longitude": [11.81210, 11.24322],
                    "recognized_address": [None, None],
                    "metadata": {"STATISTICS_MEAN": "0.0034"},
                    "message": [None, None],
                },
            ),
            (
                [(41.725469, 12.286326, None), (41.726315, 12.285276, None)],
                {
                    "band1": [-2.0, 0.02111816],
                    "band2": [-2, 0.0422363],
                    "band3": [-2, 0.06335499],
                    "latitude": [41.725469, 41.726315],
                    "longitude": [12.286326, 12.285276],
                    "addresses": [None, None],
                    "recognized_latitude": [41.725469, 41.726315],
                    "recognized_longitude": [12.286326, 12.285276],
                    "recognized_address": [None, None],
                    "metadata": {"STATISTICS_MEAN": "0.0034"},
                    "message": [None, None],
                },
            ),  # first in water, second on land
        ],
    )
    def test_read_all_bands_and_metadata(self, coordinates, want):
        gmapsgeocoder = GMapsGeocoder()
        riogeoreader = RasterIOReader()
        got = sample(
            filename="src/api/common/readgeodata/tests/fixtures/ostia_near_sea_fixture_3bands_metadata.tiff",
            tiff_tags=["STATISTICS_MEAN"],
            coordinates=coordinates,
            geocoder=gmapsgeocoder,
            geodatareader=riogeoreader,
        )

        self.compare_outputs(want=want, got=got)

    @pytest.mark.parametrize(
        "coordinates,want",
        [
            (
                [(41.51808, 11.81210, None), (42.33055, 11.24322, None)],
                {
                    "band1": [-2.0, -2.0],
                    "band2": [-2.0, -2.0],
                    "band3": [-2.0, -2.0],
                    "latitude": [41.51808, 42.33055],
                    "longitude": [11.81210, 11.24322],
                    "addresses": [None, None],
                    "recognized_latitude": [41.51808, 42.33055],
                    "recognized_longitude": [11.81210, 11.24322],
                    "recognized_address": [None, None],
                    "metadata": {},
                    "message": [None, None],
                },
            ),
            (
                [(41.725469, 12.286326, None), (41.726315, 12.285276, None)],
                {
                    "band1": [-2.0, 0.02111816],
                    "band2": [-2, 0.0422363],
                    "band3": [-2, 0.06335499],
                    "latitude": [41.725469, 41.726315],
                    "longitude": [12.286326, 12.285276],
                    "addresses": [None, None],
                    "recognized_latitude": [41.725469, 41.726315],
                    "recognized_longitude": [12.286326, 12.285276],
                    "recognized_address": [None, None],
                    "metadata": {},
                    "message": [None, None],
                },
            ),  # first in water, second on land
        ],
    )
    def test_read_all_bands_without_metadata(self, coordinates, want):
        gmapsgeocoder = GMapsGeocoder()
        riogeoreader = RasterIOReader()
        got = sample(
            filename="src/api/common/readgeodata/tests/fixtures/ostia_near_sea_fixture_3bands_metadata.tiff",
            coordinates=coordinates,
            geocoder=gmapsgeocoder,
            geodatareader=riogeoreader,
        )

        self.compare_outputs(want=want, got=got)
