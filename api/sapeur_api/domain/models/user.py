from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha1

@dataclass
class User:
    id: str = field(default_factory=lambda: sha1().hexdigest())
    username: str = field(default_factory=lambda: 'john doe')
    email: str = field(default_factory=lambda: 'john@gmail.com')
    password: str = field(default_factory=lambda: 'adminpassword')
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
