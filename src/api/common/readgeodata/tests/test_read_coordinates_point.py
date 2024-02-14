import numpy as np
import pytest
from readgeodata.interfaces import BandsNameNotFoundError
from readgeodata.rasterioreader import RasterIOReader


class TestReadCoordinatesPoint:
    def compare_outputs(self, want: dict, got: dict) -> bool:
        assert got.keys() == want.keys()

        for k, v in got.items():
            if isinstance(v, dict):
                self.compare_outputs(v, want[k])
            elif isinstance(v, str):
                assert str(v) == str(want[k])
            else:
                np.testing.assert_almost_equal(actual=v, desired=want[k], decimal=5)

    @pytest.mark.parametrize(
        "x,y,crs,want",
        [
            (4511823, 2072095, 3035, {"band1": [-2.0], "metadata": {}}),  # in water
            (
                4511823,
                2072213,
                3035,
                {"band1": [0.021118164], "metadata": {}},
            ),  # on land
            (12.286326, 41.725469, 4326, {"band1": [-2.0], "metadata": {}}),  # in water
            (
                12.285276,
                41.726315,
                4326,
                {"band1": [0.021118164], "metadata": {}},
            ),  # on land
        ],
    )
    def test_read_aal_with_single_coord(self, x, y, crs, want):
        rio = RasterIOReader()
        got = rio.sample_data_points(
            # filename="src/api/common/utils/readgeodata/tests/fixtures/ostia_near_sea_fixture_1b.tiff",
            filename="tests/fixtures/ostia_near_sea_fixture_1b.tiff",
            coordinates=[(x, y)],
            coordinates_crs=crs,
        )
        self.compare_outputs(want=want, got=got)

    @pytest.mark.parametrize(
        "coordinates,crs,want",
        [
            (
                [(4511823, 2072095), (4511823, 2072213)],
                3035,
                {"band1": [-2.0, 0.021118164], "metadata": {}},
            ),
            (
                [(12.286326, 41.725469), (12.285276, 41.726315)],
                4326,
                {"band1": [-2.0, 0.021118164], "metadata": {}},
            ),  # first in water, second on land
        ],
    )
    def test_read_multiple_coords(self, coordinates, crs, want):
        rio = RasterIOReader()
        got = rio.sample_data_points(
            # filename="src/api/common/utils/readgeodata/tests/fixtures/ostia_near_sea_fixture_1b.tiff",
            filename="tests/fixtures/ostia_near_sea_fixture_1b.tiff",
            coordinates=coordinates,
            coordinates_crs=crs,
        )
        self.compare_outputs(want=want, got=got)

    @pytest.mark.parametrize(
        "coordinates,crs,want",
        [
            (
                [(4511823, 2072095), (4511823, 2072213)],
                3035,
                {
                    "band1": [-2.0, 0.02111816],
                    "band2": [-2, 0.0422363],
                    "band3": [-2, 0.06335499],
                    "metadata": {},
                },
            ),
            (
                [(12.286326, 41.725469), (12.285276, 41.726315)],
                4326,
                {
                    "band1": [-2.0, 0.02111816],
                    "band2": [-2, 0.0422363],
                    "band3": [-2, 0.06335499],
                    "metadata": {},
                },
            ),  # first in water, second on land
        ],
    )
    def test_read_all_bands(self, coordinates, crs, want):
        rio = RasterIOReader()
        got = rio.sample_data_points(
            # filename="src/api/common/utils/readgeodata/tests/fixtures/ostia_near_sea_fixture_3bands.tiff",
            filename="tests/fixtures/ostia_near_sea_fixture_3bands.tiff",
            coordinates=coordinates,
            coordinates_crs=crs,
        )

        self.compare_outputs(want=want, got=got)

    def test_read_file_no_bands_name(self):
        rio = RasterIOReader()

        coordinates = [(4511823, 2072095)]
        crs = 3035

        with pytest.raises(BandsNameNotFoundError):
            rio.sample_data_points(
                # filename="src/api/common/utils/readgeodata/tests/fixtures/ostia_near_sea_fixture_1b_nodescriptions.tiff",
                filename="tests/fixtures/ostia_near_sea_fixture_1b_nodescriptions.tiff",
                coordinates=coordinates,
                coordinates_crs=crs,
            )

    @pytest.mark.parametrize(
        "coordinates,crs,want",
        [
            (
                [(4511823, 2072095), (4511823, 2072213)],
                3035,
                {
                    "band1": [-2.0, 0.02111816],
                    "band2": [-2, 0.0422363],
                    "band3": [-2, 0.06335499],
                    "metadata": {"STATISTICS_MEAN": "0.0034"},
                },
            ),
            (
                [(12.286326, 41.725469), (12.285276, 41.726315)],
                4326,
                {
                    "band1": [-2.0, 0.02111816],
                    "band2": [-2, 0.0422363],
                    "band3": [-2, 0.06335499],
                    "metadata": {"STATISTICS_MEAN": "0.0034"},
                },
            ),  # first in water, second on land
        ],
    )
    def test_read_all_bands_and_metadata(self, coordinates, crs, want):
        rio = RasterIOReader()
        got = rio.sample_data_points(
            # filename="src/api/common/utils/readgeodata/tests/fixtures/ostia_near_sea_fixture_3bands.tiff",
            filename="tests/fixtures/ostia_near_sea_fixture_3bands_metadata.tiff",
            metadata=["STATISTICS_MEAN"],
            coordinates=coordinates,
            coordinates_crs=crs,
        )

        self.compare_outputs(want=want, got=got)

    @pytest.mark.parametrize(
        "coordinates,crs,want",
        [
            (
                [(4511823, 2072095), (4511823, 2072213)],
                3035,
                {
                    "band1": [-2.0, 0.02111816],
                    "band2": [-2, 0.0422363],
                    "band3": [-2, 0.06335499],
                    "metadata": {},
                },
            ),
            (
                [(12.286326, 41.725469), (12.285276, 41.726315)],
                4326,
                {
                    "band1": [-2.0, 0.02111816],
                    "band2": [-2, 0.0422363],
                    "band3": [-2, 0.06335499],
                    "metadata": {},
                },
            ),  # first in water, second on land
        ],
    )
    def test_read_all_bands_and_metadata_without_metadata_param(
        self, coordinates, crs, want
    ):
        rio = RasterIOReader()
        got = rio.sample_data_points(
            # filename="src/api/common/utils/readgeodata/tests/fixtures/ostia_near_sea_fixture_3bands.tiff",
            filename="tests/fixtures/ostia_near_sea_fixture_3bands_metadata.tiff",
            coordinates=coordinates,
            coordinates_crs=crs,
        )

        self.compare_outputs(want=want, got=got)
