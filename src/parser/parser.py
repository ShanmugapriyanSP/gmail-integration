from abc import ABC, abstractmethod


class Parser(ABC):

    @staticmethod
    @abstractmethod
    def parse(*args, **kwargs):
        ...
