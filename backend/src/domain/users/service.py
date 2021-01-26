from datetime import datetime
from typing import Any, Dict, List, Union

from marshmallow import ValidationError

from domain.Users.entity import UserEntity, UserType
from domain.Users.repository import AbstractUserRepository
from domain.Users.schema import UserSchema
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
    def list_Users(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            Users: List[UserEntity] = uow.user.get_all()
            return UserService.schema(many=True).dump(Users)
