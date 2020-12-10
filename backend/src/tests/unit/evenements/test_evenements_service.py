from datetime import datetime

from domain.evenements.entity import EvenementEntity, EvenementType
from domain.evenements.repository import AbstractEvenementRepository, AlreadyExistingEvenementUuid, NotFoundEvenement
from domain.evenements.service import EvenementService
from tests.helpers.filter import filter_dict_with_keys
from uuid import uuid4
import pytest


def test_add_evenement(evenement_repo: AbstractEvenementRepository):
    uuid = str(uuid4())
    expected_title = "My title"
    expected_description = "My description"
    _type = EvenementType.NATURAL
    started_at = datetime.now()
    creator_id = str(uuid4())
    EvenementService.add_evenement(uuid=uuid,
                                   title=expected_title,
                                   description=expected_description,
                                   type=_type,
                                   started_at=started_at,
                                   creator_id=creator_id,
                                   ended_at=None,
                                   repo=evenement_repo
                                   )

    assert evenement_repo.get_all()[0] == EvenementEntity(uuid=uuid,
                                                          title=expected_title,
                                                          description=expected_description,
                                                          type=_type,
                                                          started_at=started_at,
                                                          creator_id=creator_id)


def test_fails_to_add_evenement_when_already_exists(evenement_repo: AbstractEvenementRepository):
    uuid = str(uuid4())
    expected_title = "My title"
    expected_description = "My description"
    _type = EvenementType.NATURAL
    started_at = datetime.now()
    creator_id = str(uuid4())
    evenement1 = EvenementEntity(uuid=uuid,
                                 title=expected_title,
                                 description=expected_description,
                                 type=_type,
                                 started_at=started_at,
                                 creator_id=creator_id)
    evenement_repo.add(evenement1)

    with pytest.raises(AlreadyExistingEvenementUuid):
        EvenementService.add_evenement(uuid=uuid,
                                       title=expected_title,
                                       description=expected_description,
                                       type=_type,
                                       started_at=started_at,
                                       creator_id=creator_id,
                                       ended_at=None,
                                       repo=evenement_repo)


def test_list_evenements(evenement_repo: AbstractEvenementRepository):
    evenement1_uuid = str(uuid4())
    serialized_evenement1 = {
        "uuid": evenement1_uuid,
        "title": "Evenement 1 title",
        "description": "Evenement 1 description",
        "type": EvenementType.NATURAL,
        "started_at": datetime.now(),
        "creator_id": str(uuid4()),
    }
    evenement1 = EvenementEntity(uuid=serialized_evenement1["uuid"],
                                 title=serialized_evenement1["title"],
                                 description=serialized_evenement1["description"],
                                 type=serialized_evenement1["type"],
                                 started_at=serialized_evenement1["started_at"],
                                 creator_id=serialized_evenement1["creator_id"])
    evenement_repo.add(evenement1)
    evenements = EvenementService.list_evenements(evenement_repo)

    assert len(evenements) == 1
    assert filter_dict_with_keys(evenements[0], serialized_evenement1) == serialized_evenement1


def test_get_by_uuid_when_not_present(evenement_repo: AbstractEvenementRepository):
    with pytest.raises(NotFoundEvenement):
        EvenementService.get_by_uuid("not_in_repo_uuid", evenement_repo)


def test_get_by_uuid_when_evenement_present(evenement_repo: AbstractEvenementRepository):
    evenement1_uuid = str(uuid4())
    serialized_evenement1 = {
        "uuid": evenement1_uuid,
        "title": "Evenement 1 title",
        "description": "Evenement 1 description",
        "type": EvenementType.NATURAL,
        "started_at": datetime.now(),
        "creator_id": str(uuid4()),
    }
    evenement1 = EvenementEntity(uuid=serialized_evenement1["uuid"],
                                 title=serialized_evenement1["title"],
                                 description=serialized_evenement1["description"],
                                 type=serialized_evenement1["type"],
                                 started_at=serialized_evenement1["started_at"],
                                 creator_id=serialized_evenement1["creator_id"]
                                 )
    evenement_repo.add(evenement1)

    evenement = EvenementService.get_by_uuid(evenement1_uuid, evenement_repo)
    assert filter_dict_with_keys(evenement, serialized_evenement1) == serialized_evenement1
