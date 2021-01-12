from dataclasses import dataclass, field
from typing import List, Any

from domain.core.commands import Command
from domain.core.topics import Topic, CreateMessageTopic, CreateTagTopic, \
    UploadResourceContentTopic, CreateResourceTopic


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
class UploadResourceContent(Command):
    data: dict
    topic: Topic = UploadResourceContentTopic
    file: Any = None
