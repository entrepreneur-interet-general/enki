from uuid import uuid4

from adapters.postgres.repository import PgRepositoryMixin
from domain.evenements.entities.message_entity import MessageEntity
from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.ports.message_repository import AbstractMessageRepository
from domain.evenements.ports.tag_repository import AbstractTagRepository


def test_add_message_and_add_tag(message_repo: AbstractMessageRepository, tag_repo: AbstractTagRepository):
    if isinstance(tag_repo, PgRepositoryMixin) and isinstance(message_repo, PgRepositoryMixin):
        message_uuid = str(uuid4())
        tag_uuid = str(uuid4())
        event_uuid = str(uuid4())
        message = MessageEntity(message_uuid, title="Some title", description="Some description", evenement_id=event_uuid)
        tag = TagEntity(tag_uuid, "Some title")
        message_repo.add(message)
        tag_repo.add(tag)
        added_message = message_repo.get_by_uuid(message_uuid)
        added_tag = tag_repo.get_by_uuid(tag_uuid)
        print(added_tag)
        print(added_message)

        message_repo.add_tag_to_message(message=added_message,
                                  tag=added_tag)

        message: MessageEntity = message_repo.get_by_uuid(message_uuid)
        tag: TagEntity = tag_repo.get_by_uuid(tag_uuid)

        assert message.tags[0] == tag


def test_add_message_and_failed_to_add_tag_if_already_exists(message_repo: AbstractMessageRepository):
    pass
