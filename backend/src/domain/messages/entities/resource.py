from datetime import datetime

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Optional, Literal

from domain.core.entity import Entity

content_types = [
    "application/xml",
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/gif",
    "video/x-msvideo", # AVI
]

@dataclass_json
@dataclass
class ResourceEntity(Entity):
    bucket_name: str
    object_path: str
    content_type: str
    original_name: str
    message_id: Optional[str] = field(default_factory=lambda: None)
    creator_id: Optional[str] = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.now())

    @property
    def path_without_bucket(self) -> str:
        return f"{self.prefix}/{self.object_name}"

    @property
    def complete_path(self) -> str:
        return f"{self.bucket_name}/{self.path_without_bucket}"