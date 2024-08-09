from abc import ABCMeta, abstractmethod


class BaseApiConnector(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def insert_data(self) -> None:
        pass

    @abstractmethod
    def fetch_data(self) -> None:
        pass
