import abc
from typing import Any, Hashable

# We cache the last CACHE_MAX_SIZE locations
CACHE_MAX_SIZE = 100


class Cache(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, max_size: int = 100): ...

    @abc.abstractmethod
    def get(self, key: Hashable):  # noqa: ANN201
        ...

    @abc.abstractmethod
    def set(self, key: Hashable, value: Any):  # noqa: ANN201
        ...


class LambdaCache:
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size

    def get(self, key: Hashable) -> Any:
        """Get cached value associated with input key

        Parameters
        ----------
        key : Hashable
            Hashable key used to retrieve the mapped value

        Raises
        ------
        KeyError
            if the key is not found in the cache

        Returns
        -------
        value
            Mapped value associated to key
        """
        return self.cache[key]

    def set(self, key: Hashable, value: Any) -> None:
        """Cache (key,value) couple

        Parameters
        ----------
        key : Hashable
            Hashable key used to retrieve the mapped value
        value : Any
            Value to be cached

        Returns
        -------
        None
        """
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
