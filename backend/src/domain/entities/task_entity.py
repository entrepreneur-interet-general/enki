from dataclasses import dataclass

@dataclass
class TaskEntity:
    uuid: str
    title: str
    # description: str
    # executor_id: str = field(default_factory=lambda: None)
    # creator_id: str = field(default_factory=lambda: None)
    # user_ids: str = field(default_factory=list)
    # created_at: datetime = field(default_factory=lambda: datetime.now())
    # started_at: datetime = field(default_factory=lambda: None)
    # done_at: datetime = field(default_factory=lambda: None)
    # updated_at: datetime = field(default_factory=lambda: datetime.now())