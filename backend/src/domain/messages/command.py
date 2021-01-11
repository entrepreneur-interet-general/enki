from dataclasses import dataclass, field
from typing import List

from domain.core.commands import Command
from domain.core.topics import Topic, CreateMessageTopic, CreateTagTopic


@dataclass
class CreateMessage(Command):
    data: dict
    topic: Topic = CreateMessageTopic


@dataclass
class CreateTag(Command):
    data: dict
    topic: Topic = CreateTagTopic