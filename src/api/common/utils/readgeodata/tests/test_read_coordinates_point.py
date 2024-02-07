import numpy as np
import pytest
from main import RasterIOReader


class TestReadCoordinatesPoint:
    @pytest.mark.parametrize(
        "x,y,crs,want",
        [
            (4511823, 2072095, 3035, [-2.0]),
            (4511823, 2072213, 3035, [0.021118164]),
            (12.286326, 41.725469, 4326, [-2.0]),
            (12.285276, 41.726315, 4326, [0.021118164]),
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
