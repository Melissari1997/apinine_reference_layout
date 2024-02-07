import rasterio
import rasterio.warp
from interfaces import GeoDataReader
from rasterio.crs import CRS


class RasterIOReader(GeoDataReader):
    def __init__(self):
        pass

    def sample_data_points(
        self, filename: str, coordinates: list[tuple], coordinates_crs: int = 4326
    ):
        with rasterio.open(filename) as ds:
            current_crs = ds.profile["crs"]

            # FIXME: handle multiple coordinates
            points = [list(pair) for pair in coordinates]
            feature = {
                "type": "MultiPoint",
                "coordinates": points,
            }

            # FIXME: avoid warp if same crs
            feature_proj = rasterio.warp.transform_geom(
                CRS.from_epsg(coordinates_crs), current_crs, feature
            )

            # FIXME: handle multiple bands
            sampled_data_points = ds.sample(feature_proj["coordinates"])
            values = [v[0] for v in sampled_data_points]

        return values
