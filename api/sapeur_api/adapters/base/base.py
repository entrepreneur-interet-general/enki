import abc

from typing import List


class AbstractRepository(abc.ABC):
    @abc.abstractmethod  # (1)
    def add(self, obj: object):
        raise NotImplementedError  # (2)

    @abc.abstractmethod
    def get(self, reference) -> object:
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self, query) -> List[object]:
        raise NotImplementedError
