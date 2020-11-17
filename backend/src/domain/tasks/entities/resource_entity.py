from typing import Optional, Union
from domain.core.entity import TimeStampedEntity
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

content_types = [
    "application/xml",
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/gif",
    "video/x-msvideo", # AVI
]

@dataclass
class ResourceURI:
    bucket_name: str
    path: str
    object_name: str

    @property
    def path_without_bucket(self) -> str:
        return f"{self.path}/{self.object_name}"

    @property
    def path(self) -> str:
        return f"{self.bucket_name}/{self.path_without_bucket}"


@dataclass_json
@dataclass
class ResourceEntity(TimeStampedEntity):
    title: str
    uri: ResourceURI
    content_type: str
    description: Optional[str] = field(default_factory=lambda: None)
