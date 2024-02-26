import abc


class BandsNameNotFoundError(Exception):
    pass


class GeoDataReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def sample_data_points(  # noqa: ANN201
        self, filename: str, coordinates: list[tuple], coordinates_crs: int = 4326
    ):
        pass
