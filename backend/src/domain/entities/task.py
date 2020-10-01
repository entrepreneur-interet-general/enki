from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha1


@dataclass
class Task:
    id: str = field(default_factory=lambda: sha1().hexdigest())
    creator_id: str = field(default_factory=lambda: None)
    executor_id: str = field(default_factory=lambda: None)
    title: str = field(default_factory=lambda: 'task title')
    description: str = field(default_factory=lambda: 'task description')
    user_ids: str = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now())
    started_at: datetime = field(default_factory=lambda: None)
    done_at: datetime = field(default_factory=lambda: None)
    updated_at: datetime = field(default_factory=lambda: datetime.now())
