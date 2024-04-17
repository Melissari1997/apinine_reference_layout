import abc


class UserDB(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, client: object):
        self.client = client

    @abc.abstractmethod
    def query_user(self, email: str) -> dict:
        pass
