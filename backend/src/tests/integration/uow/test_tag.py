from uuid import uuid4

from domain.tasks.entities.tag_entity import TagEntity
from service_layer.unit_of_work import AbstractUnitOfWork


def test_add_tag(uow: AbstractUnitOfWork):
    uuid = str(uuid4())
    expected_title = "My title"
    tag = TagEntity(uuid=uuid, title=expected_title,)
    with uow:
        uow.tag.add(tag)
        assert uow.tag.get_all()[0] == tag