import abc


class GeoDataReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def sample_data_points(
        self, filename: str, coordinates: list[tuple], coordinates_crs: int = 4326
    ):
        pass
