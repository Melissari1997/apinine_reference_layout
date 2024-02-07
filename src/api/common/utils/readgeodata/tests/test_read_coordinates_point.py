import numpy as np
import pytest
from rasterioreader import RasterIOReader


class TestReadCoordinatesPoint:
    @pytest.mark.parametrize(
        "x,y,crs,want",
        [
            (4511823, 2072095, 3035, [-2.0]),  # in water
            (4511823, 2072213, 3035, [0.021118164]),  # on land
            (12.286326, 41.725469, 4326, [-2.0]),  # in water
            (12.285276, 41.726315, 4326, [0.021118164]),  # on land
        ],
    )
    def test_read_aal_with_single_coord(self, x, y, crs, want):
        rio = RasterIOReader()
        got = rio.sample_data_points(
            # filename="src/api/common/utils/readgeodata/tests/fixtures/ostia_near_sea_fixture.tiff",
            filename="tests/fixtures/ostia_near_sea_fixture.tiff",
            coordinates=[(x, y)],
            coordinates_crs=crs,
        )
        np.testing.assert_almost_equal(got, want)

    @pytest.mark.parametrize(
        "coordinates,crs,want",
        [
            (
                [(4511823, 2072095), (4511823, 2072213)],
                3035,
                [-2.0, 0.021118164],
            ),
            (
                [(12.286326, 41.725469), (12.285276, 41.726315)],
                4326,
                [-2.0, 0.021118164],
            ),  # first in water, second on land
        ],
    )
    def test_read_multiple_coords(self, coordinates, crs, want):
        rio = RasterIOReader()
        got = rio.sample_data_points(
            # filename="src/api/common/utils/readgeodata/tests/fixtures/ostia_near_sea_fixture.tiff",
            filename="tests/fixtures/ostia_near_sea_fixture.tiff",
            coordinates=coordinates,
            coordinates_crs=crs,
        )
        np.testing.assert_almost_equal(got, want)

    @pytest.mark.parametrize(
        "coordinates,crs,want",
        [
            (
                [(4511823, 2072095), (4511823, 2072213)],
                3035,
                [-2.0, 0.021118164],
            ),
            (
                [(12.286326, 41.725469), (12.285276, 41.726315)],
                4326,
                [-2.0, 0.021118164],
            ),  # first in water, second on land
        ],
    )
    def test_read_all_bands(self, coordinates, crs, want):
        rio = RasterIOReader()
        got = rio.sample_data_points(
            filename="src/api/common/utils/readgeodata/tests/fixtures/ostia_near_sea_fixture_3bands.tiff",
            # filename="tests/fixtures/ostia_near_sea_fixture_3bands.tiff",
            coordinates=coordinates,
            coordinates_crs=crs,
        )
        np.testing.assert_almost_equal(got, want)
