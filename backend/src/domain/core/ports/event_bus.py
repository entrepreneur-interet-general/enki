import abc
import logging
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Callable, Coroutine, Dict, Generic, List, Generic

from flask import current_app

from domain.core import commands, events
from domain.core.events import EventCallback, Event
from domain.core.topics import Topic
from typing import Union, Callable

from service_layer.unit_of_work import AbstractUnitOfWork

Message = Union[commands.Command, events.Event]


class AbstractEventBus(abc.ABC):
    @abc.abstractmethod
    def subscribe(self, topic: Topic, callback: EventCallback) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def publish(self, event: Event, uow: AbstractUnitOfWork = None) -> None:
        raise NotImplementedError


class InMemoryEventBus(AbstractEventBus):
    def __init__(self) -> None:
        super().__init__()
        self._subscriptions: Dict[Topic, List[EventCallback]] = defaultdict(lambda: [])

    def subscribe(self, topic: Topic, callback: EventCallback) -> None:
        print(f"Subscribes to {topic} with {callback}")
        self._subscriptions[topic].append(callback)

    def publish(self, message: Message, uow: AbstractUnitOfWork = None) -> List[Any]:
        results = []
        current_app.logger.info("test")
        current_app.logger.info(self._subscriptions[message.topic])

        for callback in set(self._subscriptions[message.topic]):
            current_app.logger.debug(f"callback {callback}")
            if isinstance(message, events.Event):
                self._handle_event(message, callback=callback)
            elif isinstance(message, commands.Command):
                result = self._handle_command(message, callback=callback, uow=uow)
                results.append(result)
            else:
                raise Exception(f'{message} was not an Event or Command')
        return results

    @staticmethod
    def _handle_event(event: events.Event, callback: Callable):
        try:
            current_app.logger.debug('handling event %s with handler %s', event, callback)
            callback(event)
        except Exception:
            current_app.logger.exception('Exception handling event %s', event)

    @staticmethod
    def _handle_command(command: commands.Command, callback: Callable, uow: AbstractUnitOfWork):
        current_app.logger.debug('handling command %s', command)
        try:
            result = callback(command, uow=uow)
            return result  # (3)
        except Exception:
            current_app.logger.exception('Exception handling command %s', command)
            raise  # (2)
