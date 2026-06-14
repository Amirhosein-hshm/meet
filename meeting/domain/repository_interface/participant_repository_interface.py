from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from domain.entity.meet_entity import Meet


@dataclass
class ParticipantData:
    meet_id: int
    user_id: int
    is_banned: bool
    joined_at: Optional[datetime] = None


class IParticipantRepository(ABC):
    @abstractmethod
    def get_user_invitations(self, user_id: int) -> List[Meet]:
        pass

    @abstractmethod
    def find_participant(self, meet_id: int, user_id: int) -> Optional[ParticipantData]:
        pass

    @abstractmethod
    def is_user_banned(self, meet_id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    def ban_user(self, meet_id: int, user_id: int) -> None:
        pass