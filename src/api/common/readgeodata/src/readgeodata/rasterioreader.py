import numpy as np
import rasterio
import rasterio.warp
from rasterio.crs import CRS

from readgeodata.interfaces import BandsNameNotFoundError, GeoDataReader


class RasterIOReader(GeoDataReader):
    def __init__(self):
        pass

    def sample_data_points(
        self,
        filename: str,
        coordinates: list[tuple],
        metadata: list[str] = None,
        coordinates_crs: int = 4326,
    ) -> dict:
        """Sample a .tif file at specific coordinates.

        This does the following:
        - Open the file
        - Transform the coordinates in the provided CRS
        - Sample the data points from the file
        - Include any provided metadata

        Parameters
        ----------
        filename : str
            Path of the file to be read.
        coordinates : list[tuple]
            List of tuples in the form (lon, lat).
        metadata : list[str], optional
            Metadatas to fetch from file, by default None.
        coordinates_crs : int, optional
            CRS of the provided coordinates, by default 4326.

        Returns
        -------
        dict
            Dictionary of data mapping the .tif band names to a list of values
            sampled at specified coordinates. Any additional metadata included
            as arguments is included in a 'metadata' field, which is a dictionary
            mapping metadata fields and values found in the .tif file.

        Raises
        ------
        BandsNameNotFoundError
            Raised when any of the tif file's bands has no name.
        """
        if metadata is None:
            metadata = []

        with rasterio.open(filename) as ds:
            current_crs = ds.profile["crs"]
            tags = {tag: ds.tags()[tag] for tag in metadata}

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
            output = dict(zip(ds.descriptions, t, strict=False), **{"metadata": tags})

        return output
