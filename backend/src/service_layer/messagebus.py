from typing import List, Dict, Callable, Type
from domain.core.topics import Topic
from domain.core import topics
from .handlers import events, commands

EVENT_HANDLERS: Dict[Type[Topic], List[Callable]] = {
    topics.AffairCreatedTopic: [
        events.send_affair_created_email_notification,
        # handlers.send_ack_message_to_sge_on_affair_received
        # handlers.send_affair_created_sms_notification],
    ],
}

COMMAND_HANDLERS: Dict[Type[Topic], List[Callable]] = {
    topics.CreateEvenementTopic: [
        commands.create_evenement,
    ],
    topics.CreateTaskTopic: [
        commands.create_task,
    ],
    topics.CreateTagTopic: [
        commands.create_tag,
    ],
}

HANDLERS: Dict[Type[Topic], List[Callable]] = {**EVENT_HANDLERS, **COMMAND_HANDLERS}
