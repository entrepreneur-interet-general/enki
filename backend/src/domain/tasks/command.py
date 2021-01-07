from dataclasses import dataclass
from typing import List

from domain.core.commands import Command
from domain.core.topics import Topic, CreateTaskTopic, CreateTagTopic, CreateInformationTopic


@dataclass
class CreateTask(Command):
    data: dict
    tags: List[str]
    topic: Topic = CreateTaskTopic


@dataclass
class CreateTag(Command):
    data: dict
    topic: Topic = CreateTagTopic

@dataclass
class CreateInformation(Command):
    data: dict
    topic: Topic = CreateInformationTopic
