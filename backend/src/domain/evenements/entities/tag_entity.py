from dataclasses import dataclass, field
from datetime import datetime
from typing import Union, Optional

from dataclasses_json import dataclass_json
from slugify import slugify

from domain.core.entity import Entity


@dataclass_json
@dataclass
class TagEntity(Entity):
    title: str
    slug: str = field(init=False)
    creator_id: Optional[None] = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def __post_init__(self):
        self.slug = slugify(self.title)
