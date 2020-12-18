from dataclasses import dataclass
from domain.core.commands import Command
from domain.core.topics import Topic, CreateTaskTopic, CreateTagTopic


@dataclass
class CreateTask(Command):
    data: dict
    topic: Topic = CreateTaskTopic


@dataclass
class CreateTag(Command):
    data: dict
    topic: Topic = CreateTagTopic
