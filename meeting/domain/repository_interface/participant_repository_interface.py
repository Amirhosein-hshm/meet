from abc import ABC, abstractmethod
from typing import List

from domain.entity.meet_entity import Meet


class IParticipantRepository(ABC):
    @abstractmethod
    def get_user_invitations(self, user_id: int) -> List[Meet]:
        pass