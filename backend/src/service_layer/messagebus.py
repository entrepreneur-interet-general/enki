from typing import List, Dict, Callable, Type
from domain.core.topics import Topic
from domain.core import topics
from . import handlers

HANDLERS: Dict[Type[Topic], List[Callable]] = {
    topics.AffairCreatedTopic: [
        handlers.send_affair_created_email_notification,
        # handlers.send_ack_message_to_sge_on_affair_received
        # handlers.send_affair_created_sms_notification],
    ],
}
