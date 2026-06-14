from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Tuple

from domain.entity.meet_entity import Meet
from domain.entity.user_entity import Role


@dataclass
class MeetFilter:
    actor_id: int
    actor_role: Role
    creator_id: Optional[int] = None
    participant_user_id: Optional[int] = None
    start_date_from: Optional[datetime] = None
    start_date_to: Optional[datetime] = None
    guest_username: Optional[str] = None
    title_query: Optional[str] = None


class IMeetRepository(ABC):
    @abstractmethod
    def save(self, meet: Meet) -> Meet:
        pass

    @abstractmethod
    def find_by_hash(self, meet_hash: str) -> Optional[Meet]:
        pass

    @abstractmethod
    def find_by_id(self, meet_id: int) -> Optional[Meet]:
        pass

    @abstractmethod
    def delete(self, meet_id: int) -> None:
        pass

    @abstractmethod
    def find_paginated(self, filters: MeetFilter, page: int, size: int) -> Tuple[List[Meet], int]:
        pass
