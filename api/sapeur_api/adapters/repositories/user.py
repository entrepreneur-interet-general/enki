from typing import List

from ...domain.models.user import User
from ..repository import AbstractRepository


class UserRepository(AbstractRepository):

    def get(self, reference) -> User:
        pass

    def add(self, user: User):
        pass

    def find_all(self, query) -> List[object]:
        pass
