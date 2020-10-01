from typing import List

from ....domain.models.user import User
from ...base.sql import AbstractSQLRepository
from ...models.user import users_lines

class UserRepository(AbstractSQLRepository):

    def __init__(self, db):
        super().__init__(db)

    def get(self, reference) -> User:
        pass

    def add(self, user: User):
        pass

    def find_all(self, query) -> List[object]:
        pass
