from dataclasses import dataclass
from datetime import datetime

from domain.entity.user_entity import Role
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import ResourceNotFoundError


@dataclass
class GetUserByUsernameRequestInput:
    actor_id: int
    actor_role: Role
    username: str


@dataclass
class GetUserByUsernameResponseOutput:
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    update_at: datetime


class GetUserByUsernameUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, request: GetUserByUsernameRequestInput) -> GetUserByUsernameResponseOutput:
        user = self.user_repository.find_by_username(request.username)
        if not user:
            raise ResourceNotFoundError(f"کاربر با نام کاربری '{request.username}' یافت نشد.")

        return GetUserByUsernameResponseOutput(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            role=user.role.value,
            is_active=user.is_active,
            created_at=user.created_at,
            update_at=user.update_at,
        )
