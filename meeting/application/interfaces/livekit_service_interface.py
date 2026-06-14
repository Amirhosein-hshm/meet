from abc import ABC, abstractmethod


class ILiveKitService(ABC):
    @abstractmethod
    def generate_join_token(self, identity: str, room_name: str, room_admin: bool = False) -> str:
        pass

    @abstractmethod
    def remove_participant(self, room_name: str, identity: str) -> None:
        pass
