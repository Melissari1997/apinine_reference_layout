import numpy as np
import rasterio
import rasterio.warp
from rasterio.crs import CRS

from .interfaces import BandsNameNotFoundError, GeoDataReader


class RasterIOReader(GeoDataReader):
    def __init__(self):
        pass

    def sample_data_points(
        self, filename: str, coordinates: list[tuple], coordinates_crs: int = 4326
    ):
        with rasterio.open(filename) as ds:
            current_crs = ds.profile["crs"]

            points = [list(pair) for pair in coordinates]
            feature = {
                "type": "MultiPoint",
                "coordinates": points,
            }

            # FIXME: avoid warp if same crs
            feature_proj = rasterio.warp.transform_geom(
                CRS.from_epsg(coordinates_crs), current_crs, feature
            )

            descriptions = ds.descriptions
            if not all(descriptions):
                raise BandsNameNotFoundError(f"Cannot find bands name in {filename}")

            # sampled points response is N x B where:
            # - N is the number of coordinates
            # - and B the number of bands
            # we want the output to be shaped as B x N
            sampled_data_points = ds.sample(feature_proj["coordinates"])
            mat = np.array(list(sampled_data_points))
            t = mat.T
            output = dict(zip(ds.descriptions, t, strict=False))

        return output
