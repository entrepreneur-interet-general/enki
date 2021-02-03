from typing import Any, Dict, List
from domain.users.entities.group import GroupEntity, GroupType
from domain.users.schemas.group import GroupSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class GroupService:
    schema = GroupSchema

    @staticmethod
    def list_groups(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            groups: List[GroupEntity] = uow.group.get_all()
            return GroupService.schema(many=True).dump(groups)

    @staticmethod
    def list_group_types(uow: AbstractUnitOfWork) -> List[str]:
        with uow:
            return [e.value for e in list(GroupType)]
