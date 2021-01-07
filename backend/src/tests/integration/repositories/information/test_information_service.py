from domain.tasks.entities.info_entity import InformationEntity
from domain.tasks.ports.information_repository import AlreadyExistingInformationUuid, NotFoundInformation, \
    AbstractInformationRepository
from domain.tasks.services.information_service import InformationService
from tests.helpers.filter import filter_dict_with_keys
from uuid import uuid4
import pytest


def test_add_information(information_repo: AbstractInformationRepository):
    uuid = str(uuid4())
    expected_title = "My title"
    expected_description = "My description"
    expected_event = "event_id"
    information = InformationEntity(uuid,
                                    title=expected_title,
                                    description=expected_description,
                                    evenement_id=expected_event
                                    )
    information_repo.add(information)

    assert information_repo.get_all()[0] == information


def test_fails_to_add_information_when_already_exists(information_repo: AbstractInformationRepository):
    information1_uuid = str(uuid4())
    serialized_information1 = {
        "uuid": information1_uuid,
        "title": "Information 1 title",
        "description": "Information 1 description",
        "evenement_id": "event_id"
    }
    information1 = InformationEntity(uuid=information1_uuid,
                                     title=serialized_information1["title"],
                                     description=serialized_information1["description"],
                                     evenement_id=serialized_information1["evenement_id"],
                                     )
    information_repo.add(information1)

    with pytest.raises(AlreadyExistingInformationUuid):
        information_repo.add(information1)


def test_list_informations(information_repo: AbstractInformationRepository):
    information1_uuid = str(uuid4())
    serialized_information1 = {
        "uuid": information1_uuid,
        "title": "Information 1 title",
        "description": "Information 1 description",
        "evenement_id": "event_id"
    }
    information1 = InformationEntity(uuid=information1_uuid,
                                     title=serialized_information1["title"],
                                     description=serialized_information1["description"],
                                     evenement_id=serialized_information1["evenement_id"],

                                     )
    information_repo.add(information1)

    informations = information_repo.get_all()

    assert len(informations) == 1
    assert informations[0] == information1


def test_get_by_uuid_when_not_present(information_repo: AbstractInformationRepository):
    with pytest.raises(NotFoundInformation):
        information_repo.get_by_uuid("not_in_repo_uuid")


def test_get_by_uuid_when_information_present(information_repo: AbstractInformationRepository):
    information1_uuid = str(uuid4())
    serialized_information1 = {
        "uuid": information1_uuid,
        "title": "Information 1 title",
        "description": "Information 1 description",
        "evenement_id": "event_id"

    }
    information1 = InformationEntity(uuid=information1_uuid,
                                     title=serialized_information1["title"],
                                     description=serialized_information1["description"],
                                     evenement_id=serialized_information1["evenement_id"],

                                     )
    information_repo.add(information1)

    information = information_repo.get_by_uuid(information1_uuid)
    assert information == information1
