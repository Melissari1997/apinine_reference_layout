import abc
import json
from typing import Dict, Iterable

import geopandas as gpd
import rasterio
from bream.core import Box
from shapely.geometry import shape


class MapConverter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def convert(): ...  # noqa: ANN201


class GeoJSONConverter(MapConverter):
    def convert(
        self,
        data: Iterable,
        profile: dict,
        box_3035_to_clip: Box,
        target_crs: int,
        metadata: dict = None,
    ) -> Dict:
        """Convert input data to GeoJSON forma using provided profile, box and target crs.

        Parameters
        ----------
        data : array, dataset object, Band, or tuple
            GeoJSON data
        profile : dict
            profile containing geodata information
        box_3035_to_clip : Box
            Box used to restrict the geometry to a certain area
        target_crs : int
            target CRS
        metadata : dict, optional
            Additional metadata, by default None
            They will be included in a custom "metadata" key inside the GeoJSON.
            We expect this to be a dictionary in the form {"min_value": MIN_LAYER_VALUE, "max_value": MAX_LAYER_VALUE}

        Returns
        -------
        dict
            Dictionary in geojson format and a "metadata" key
        """
        if metadata is None:
            metadata = {}

        shapes_values = (
            (shape(s), v)
            for s, v in rasterio.features.shapes(data, transform=profile["transform"])
        )

        df = gpd.pd.DataFrame(shapes_values, columns=["geometry", "values"])
        gdf = (
            gpd.GeoDataFrame(df["values"], geometry=df.geometry, crs=profile["crs"])
            .clip(box_3035_to_clip)
            .to_crs(target_crs)
        )
        return {**json.loads(gdf.to_json()), "metadata": metadata}
