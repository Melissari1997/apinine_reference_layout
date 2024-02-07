import abc


class Geocoder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def geocode(self, address: str) -> tuple[tuple[float, float], str]:
        raise NotImplementedError
