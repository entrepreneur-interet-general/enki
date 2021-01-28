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
class CreateMessageTopic(Topic):
    name: str = "CreateMessage"


@dataclass
class CreateTagTopic(Topic):
    name: str = "CreateTag"


@dataclass
class AddTagToMessageTopic(Topic):
    name: str = "AddTagToMessage"


@dataclass
class CreateResourceTopic(Topic):
    name: str = "CreateResource"


@dataclass
class CreateUserTopic(Topic):
    name: str = "CreateUser"
