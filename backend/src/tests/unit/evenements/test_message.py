import pytest

from domain.evenements.entities.evenement_entity import EvenementEntity, EvenementClosedException
from domain.evenements.entities.message_entity import MessageEntity, TagAlreadyInThisMessage, NotFoundTagInThisMessage
from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.schemas import MessageSchema


def test_message_load(message_data):
    message: MessageEntity = MessageSchema().load(message_data)
    assert isinstance(message, MessageEntity)
    assert message.title == message_data["title"]


def test_add_tag(message: MessageEntity, tag_factory):
    tag1 = tag_factory()
    message.add_tag(tag=tag1)
    assert len(message.tags) == 1
    assert message.get_tag_by_id(uuid=tag1.uuid) == tag1
    with pytest.raises(TagAlreadyInThisMessage):
        message.add_tag(tag=tag1)
    tag2 = tag_factory()
    message.add_tag(tag=tag2)
    assert len(message.tags) == 2
    assert message.tags == [tag1, tag2]


def test_remove_tag(message: MessageEntity, tag_factory):
    tag1 = tag_factory()
    message.add_tag(tag=tag1)
    message.remove_tag(tag=tag1)
    assert len(message.tags) == 0
    with pytest.raises(NotFoundTagInThisMessage):
        message.get_tag_by_id(uuid=tag1.uuid)


def test_add_resource():
    pass


def test_remove_resource():
    pass


def test_cant_assign_to_closed_evenement(evenement: EvenementEntity, message_factory):
    m1: MessageEntity = message_factory()
    m2: MessageEntity = message_factory()
    m1.assign_evenement(evenement=evenement)
    assert m1.evenement_id == evenement.uuid
    evenement.close()
    with pytest.raises(EvenementClosedException):
        m2.assign_evenement(evenement=evenement)


