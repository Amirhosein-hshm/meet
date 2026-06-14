from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class Role(str, Enum):
    SuperAdmin = "SuperAdmin"
    Admin = "Admin"
    Host = "Host"
    User = "User"


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    username: str
    password_hash: str
    role: Role
    is_active: bool = False
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    update_at: datetime = field(default_factory=datetime.utcnow)

    def activate(self):
        self.is_active = True 


