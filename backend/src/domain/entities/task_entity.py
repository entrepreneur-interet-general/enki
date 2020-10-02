from dataclasses import dataclass, field
# from datetime import datetime
from uuid import uuid4


@dataclass
class TaskEntity:
    title: str
    # description: str
    uuid: str = field(default_factory = lambda: str(uuid4()))
    # executor_id: str = field(default_factory=lambda: None)
    # creator_id: str = field(default_factory=lambda: None)
    # user_ids: str = field(default_factory=list)
    # created_at: datetime = field(default_factory=lambda: datetime.now())
    # started_at: datetime = field(default_factory=lambda: None)
    # done_at: datetime = field(default_factory=lambda: None)
    # updated_at: datetime = field(default_factory=lambda: datetime.now())