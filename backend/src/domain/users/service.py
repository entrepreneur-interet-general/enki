from typing import Any, Dict, List
from marshmallow import ValidationError

from domain.users.entity import UserEntity
from domain.users.schema import UserSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class UserService:
    schema = UserSchema

    @staticmethod
    def add_user(data: dict,
                 uow: AbstractUnitOfWork):
        try:
            user: UserEntity = UserService.schema().load(data)
            return_value = UserService.schema().dump(user)
        except ValidationError as ve:
            raise ve

        with uow:
            _ = uow.user.add(user)
        return return_value

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            return UserService.schema().dump(uow.user.get_by_uuid(uuid=uuid))

    @staticmethod
    def list_users(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            users: List[UserEntity] = uow.user.get_all()
            return UserService.schema(many=True).dump(users)
