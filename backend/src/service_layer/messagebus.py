from typing import List, Dict, Callable, Type
from domain.core.topics import Topic
from domain.core import topics
from .handlers import events, commands

EVENT_HANDLERS: Dict[Type[Topic], List[Callable]] = {
    topics.AffairCreatedTopic: [
        events.send_affair_created_email_notification,
    ],
}

COMMAND_HANDLERS: Dict[Type[Topic], List[Callable]] = {
    topics.CreateEvenementTopic: [
        commands.create_evenement,
    ],
    topics.CreateMessageTopic: [
        commands.create_message,
    ],
    topics.CreateTagTopic: [
        commands.create_tag,
    ],
    topics.CreateResourceTopic: [
        commands.create_resource,
    ],
    topics.CreateUserTopic: [
        commands.create_user,
    ],
    topics.CreateContactTopic: [
        commands.create_contact,
    ],
}

HANDLERS: Dict[Type[Topic], List[Callable]] = {**EVENT_HANDLERS, **COMMAND_HANDLERS}
