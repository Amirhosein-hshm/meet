from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import uuid



@dataclass
class Meet:
    title: str
    creator_id: int
    start_time: datetime
    expires_at: datetime
    id: Optional[int] = None
    meet_hash: str = field(default_factory=lambda: uuid.uuid4().hex) 
    participants_ids: List[int] = field(default_factory=list) 
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    update_at: datetime = field(default_factory=datetime.utcnow)

    # --- Domain Logic ---
    def is_valid_for_join(self) -> bool:
        now = datetime.utcnow()
        return self.is_active and (self.start_time <= now <= self.expires_at)

    def can_user_join(self, user_id: int) -> bool:
        return user_id == self.creator_id or user_id in self.participants_ids

    def add_participant(self, user_id: int):
        if user_id not in self.participants_ids:
            self.participants_ids.append(user_id)
            self.update_at = datetime.utcnow()

    def remove_participant(self, user_id: int):
        if user_id in self.participants_ids:
            self.participants_ids.remove(user_id)
            self.update_at = datetime.utcnow()
            
    def cancel_meet(self):
        self.is_active = False
        self.update_at = datetime.utcnow()