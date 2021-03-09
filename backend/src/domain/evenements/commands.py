from dataclasses import dataclass

from domain.core.commands import Command
from domain.core.topics import Topic, CreateMessageTopic, CreateTagTopic, \
    CreateResourceTopic, CreateEvenementTopic


@dataclass
class CreateMessage(Command):
    data: dict
    topic: Topic = CreateMessageTopic


@dataclass
class CreateTag(Command):
    data: dict
    topic: Topic = CreateTagTopic


@dataclass
class CreateResource(Command):
    data: dict
    topic: Topic = CreateResourceTopic


@dataclass
class CreateEvenement(Command):
    data: dict
    topic: Topic = CreateEvenementTopic
