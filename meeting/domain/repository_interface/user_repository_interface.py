
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from domain.entity.user_entity import User


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_all_paginated(self, page: int, size: int) -> Tuple[List[User], int]:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
