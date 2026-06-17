from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from domain.entity.meet_entity import Meet


@dataclass
class ParticipantData:
    meet_id: int
    user_id: int
    joined_at: Optional[datetime] = None


class IParticipantRepository(ABC):
    @abstractmethod
    def get_user_invitations(self, user_id: int) -> List[Meet]:
        pass

    @abstractmethod
    def find_participant(self, meet_id: int, user_id: int) -> Optional[ParticipantData]:
        pass