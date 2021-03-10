import pytest

from domain.users.entities.contact import ContactEntity
from domain.users.entities.user import UserEntity, ThisUserAlreadyFavoriteThisContact, ThisUserDoesNotFavoriteThisContact
from domain.users.schemas.user import UserSchema


def test_user_load(user_data: dict):
    user: UserEntity = UserSchema().load(user_data)
    assert isinstance(user, UserEntity)
    assert user.first_name == user_data["first_name"]


def test_add_contact(user: UserEntity, contact_factory):
    contact1 = contact_factory()
    contact2 = contact_factory()
    user.add_contact(contact1)
    assert len(user.contacts) == 1
    assert user.contacts == [contact1]
    user.add_contact(contact2)
    assert len(user.contacts) == 2
    assert contact2 in user.contacts
    with pytest.raises(ThisUserAlreadyFavoriteThisContact):
        user.add_contact(contact2)


def test_remove_contact(user: UserEntity, contact: ContactEntity):
    user.add_contact(contact)
    user.remove_contact(contact)
    assert len(user.contacts) == 0
    with pytest.raises(ThisUserDoesNotFavoriteThisContact):
        user.remove_contact(contact)



