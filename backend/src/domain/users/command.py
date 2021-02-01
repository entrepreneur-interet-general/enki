from dataclasses import dataclass

from domain.core.commands import Command

from domain.core.topics import CreateUserTopic, CreateContactTopic, Topic


@dataclass
class CreateUser(Command):
    data: dict
    topic: Topic = CreateUserTopic


@dataclass
class CreateContact(Command):
    data: dict
    topic: Topic = CreateContactTopic
