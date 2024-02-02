import abc


class KeyDB(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def query_by_key(self, key: str):
        pass

    @abc.abstractmethod
    def update_last_accessed(self, last_accessed_ts: int, user: str, hash_key: str):
        pass


class Authenticator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def authorize(self, key: str, method: str, resource: str):
        pass
