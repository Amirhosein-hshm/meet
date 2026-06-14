from abc import ABC, abstractmethod

class IRefreshTokenRepository(ABC):
    @abstractmethod
    def save(self, user_id: int, token: str) -> None:
        pass

    @abstractmethod
    def is_valid(self, user_id: int, token: str) -> bool:
        pass

    @abstractmethod
    def revoke(self, user_id: int, token: str) -> None:
        pass