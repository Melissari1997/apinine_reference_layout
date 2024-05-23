import abc
from typing import Iterable, Tuple

import bream.image.raster2 as brast
from bream.core import Box
from cache import Cache


class MapReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self) -> Iterable: ...


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
        box_3035: Box,
    ) -> Tuple[Iterable, dict]:
        """Read file in

        _extended_summary_

        Parameters
        ----------
        filename : str
            _description_
        box_3035 : Box
            _description_

        Returns
        -------
        Tuple[Iterable, dict]
            _description_
        """
        # An entry is cached if the filename is the same, and the location boxes are the same
        key = (filename, tuple(box_3035.total_bounds))
        # Search the cache
        try:
            raster, profile = self.cache.get(key)
        except KeyError:
            # TODO: Investigate why it takes up to 16 seconds to read_portion from wildfire lookup
            raster, profile = brast.read_portion(
                path=filename, location_boxes=box_3035
            )[0]
            self.cache.set(key=key, value=(raster, profile))

        return raster, profile
