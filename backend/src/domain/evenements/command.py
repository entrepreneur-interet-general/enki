from dataclasses import dataclass

from domain.core.commands import Command

from domain.core.topics import CreateEvenementTopic, Topic


@dataclass
class CreateEvenement(Command):
    data: dict
    topic: Topic = CreateEvenementTopic
