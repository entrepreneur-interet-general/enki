from dataclasses import dataclass
from typing import Any, Callable, Coroutine

EventCallback = Callable[[Any], Coroutine[Any, Any, Any]]


@dataclass
class Topic:
    """

    """
    name: str


@dataclass
class AffairCreatedTopic(Topic):
    name: str = "AffairCreated"


@dataclass
class CreateEvenementTopic(Topic):
    name: str = "CreateEvenement"


@dataclass
class CreateTaskTopic(Topic):
    name: str = "CreateTask"


@dataclass
class CreateTagTopic(Topic):
    name: str = "CreateTag"


@dataclass
class CreateInformationTopic(Topic):
    name: str = "CreateInformation"


@dataclass
class AddTagToTaskTopic(Topic):
    name: str = "AddTagToTask"
