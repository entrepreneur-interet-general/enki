import abc
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Callable, Coroutine, Dict, Generic, List, Generic

from flask import current_app

from domain.core.events import EventCallback, Event
from domain.core.topics import Topic


class AbstractEventBus(abc.ABC):
    @abc.abstractmethod
    def subscribe(self, topic: Topic, callback: EventCallback) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def publish(self, event: Event) -> None:
        raise NotImplementedError


class InMemoryEventBus(AbstractEventBus):
    def __init__(self) -> None:
        super().__init__()
        self._subscriptions: Dict[Topic, List[EventCallback]] = defaultdict(lambda: [])

    def subscribe(self, topic: Topic, callback: EventCallback) -> None:
        self._subscriptions[topic].append(callback)

    def publish(self, event: Event) -> None:
        for callback in self._subscriptions[event.topic]:
            try:
                callback(event)
            except Exception as e:
                current_app.logger.error(e)
                pass
