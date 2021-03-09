import pytest

from domain.evenements.entities.evenement_entity import EvenementEntity, EvenementClosedException, UserEvenementRole, \
    EvenementRoleType
from domain.evenements.entities.message_entity import MessageEntity, TagAlreadyInThisMessage, NotFoundTagInThisMessage
from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.schemas import MessageSchema, EvenementSchema
from domain.users.entities.user import UserEntity


def test_evenement_load(evenement_data):
    evenement: EvenementEntity = EvenementSchema().load(evenement_data)
    assert isinstance(evenement, EvenementEntity)
    assert evenement.title == evenement_data["title"]


def test_evenement_closed(evenement: EvenementEntity):
    assert not evenement.closed
    evenement.close()
    assert evenement.closed
    with pytest.raises(EvenementClosedException):
        assert evenement.check_can_assign()


def test_user_roles(user: UserEntity, evenement: EvenementEntity):
    user_event_role = UserEvenementRole(
        uuid="test_id",
        user_id=user.uuid,
        evenement_id=evenement.uuid,
        type=EvenementRoleType.VIEW
    )
    evenement.add_user_role(user_event_role)

    assert evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.VIEW)
    assert not evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.EDIT)
    assert not evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.ADMIN)
    evenement.change_access_type(user_id=user.uuid, role_type=EvenementRoleType.EDIT)
    assert evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.VIEW)
    assert evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.EDIT)
    assert not evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.ADMIN)
    evenement.change_access_type(user_id=user.uuid, role_type=EvenementRoleType.ADMIN)
    assert evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.VIEW)
    assert evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.EDIT)
    assert evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.ADMIN)
    evenement.revoke_user_access(user_id=user.uuid)
    assert not evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.VIEW)
    assert not evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.EDIT)
    assert not evenement.user_has_access(user_id=user.uuid, role_type=EvenementRoleType.ADMIN)
