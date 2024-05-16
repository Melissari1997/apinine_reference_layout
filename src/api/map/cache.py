import abc
from typing import Iterable, Tuple

# We cache the last CACHE_MAX_SIZE locations
CACHE_MAX_SIZE = 100


class Cache(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, max_size: int = 100):
        pass

    @abc.abstractmethod
    def get(self, key: tuple[str, float, float]):  # noqa: ANN201
        pass

    @abc.abstractmethod
    def set(self, key: tuple[str, float, float], value: Iterable):  # noqa: ANN201
        pass


class LambdaCache:
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size

    def get(self, key: tuple[str, float, float]) -> Tuple[Iterable, dict] | None:
        return self.cache[key]

    def set(self, key: tuple[str, float, float], value: Tuple[Iterable, dict]) -> None:
        if len(self.cache) >= self.max_size:
            # If cache is full, remove the oldest item
            self.remove_oldest()
        # Set the key-value pair in cache
        self.cache[key] = value

    def remove_oldest(self) -> None:
        # Remove the oldest item from cache
        oldest_key = next(iter(self.cache))
        del self.cache[oldest_key]


cache = LambdaCache(max_size=CACHE_MAX_SIZE)
