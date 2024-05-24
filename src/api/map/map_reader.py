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
        """Read file in specified box and return data associated with it.

        The bream.raster2.read_portion function is used to read from the box.
        A cache is used to retrieve recently-accessed data.

        Parameters
        ----------
        filename : str
            Path of the file to read
        box_3035 : Box
            Box specifying the requested area

        Returns
        -------
        Tuple[Iterable, dict]
            Raster and profile of requested data
        """
        # An entry is cached if it shares filename and location boxes with a previous entry
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
