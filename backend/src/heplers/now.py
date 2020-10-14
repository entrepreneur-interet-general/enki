import abc
from datetime import datetime

class AbstractNow(abc.ABC):
    @abc.abstractclassmethod
    def get(self) -> datetime:
        raise NotImplementedError

class CustomNow(AbstractNow):
    next_date: datetime = datetime.now()

    def get(self) -> datetime:
        return self.next_date

    def set_next_date(self, date: datetime):
        self.next_date = date