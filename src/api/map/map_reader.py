import abc
from typing import Iterable, Tuple

import bream.image.raster2 as brast
from bream.core import Box
from cache import Cache


class MapReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self) -> Iterable:
        pass


class BreamMapReader(MapReader):
    def __init__(
        self,
        cache: Cache,
    ):
        self.cache = cache

    def get_box(self) -> Box:
        return self.box_3035

    def read(
        self,
        filename: str,
        lat: float,
        lon: float,
        box_3035: Box,
    ) -> Tuple[Iterable, dict]:

        # Search the cache
        try:
            raster, profile = self.cache.get((filename, lat, lon))
        except KeyError:
            # TODO: Investigate why it takes up to 16 seconds to read_portion from wildfire lookup
            raster, profile = brast.read_portion(
                path=filename, location_boxes=box_3035
            )[0]
            self.cache.set((filename, lat, lon), (raster, profile))

        return raster, profile
