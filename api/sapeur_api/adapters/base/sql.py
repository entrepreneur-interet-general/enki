import abc

from typing import List


class AbstractSQLRepository(abc.ABC):
    def __init__(self, db):
        self.db = db

    def session(self):
        return self.db.session

    @abc.abstractmethod
    def add(self, obj: object):
        self.session().add(obj)
        self.session().commit()

    @abc.abstractmethod
    def get(self, reference) -> object:
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self, query) -> List[object]:
        raise NotImplementedError
