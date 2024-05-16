import abc
import json
from typing import Iterable

import geopandas as gpd
import rasterio
from bream.core import Box
from shapely.geometry import shape


class MapConverter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def convert():  # noqa: ANN201
        pass


class GeoJSONConverter(MapConverter):
    def convert(
        self,
        data: Iterable,
        profile: dict,
        box_3035_to_clip: Box,
        target_crs: int,
        metadata: dict = None,
    ) -> Iterable:
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
        # TODO: avoid this .loads and assign this to the response body
        return {**json.loads(gdf.to_json()), "metadata": metadata}
