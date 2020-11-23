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
