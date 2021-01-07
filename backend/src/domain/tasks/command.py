from dataclasses import dataclass, field
from typing import List

from domain.core.commands import Command
from domain.core.topics import Topic, CreateTaskTopic, CreateTagTopic, CreateInformationTopic


@dataclass
class CreateTask(Command):
    data: dict
    topic: Topic = CreateTaskTopic


@dataclass
class CreateTag(Command):
    data: dict
    topic: Topic = CreateTagTopic


@dataclass
class CreateInformation(Command):
    data: dict
    topic: Topic = CreateInformationTopic
