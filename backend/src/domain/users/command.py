from dataclasses import dataclass

from domain.core.commands import Command

from domain.core.topics import CreateUserTopic, Topic


@dataclass
class CreateUser(Command):
    data: dict
    topic: Topic = CreateUserTopic
