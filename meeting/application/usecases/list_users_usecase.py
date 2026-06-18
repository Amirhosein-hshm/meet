from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from domain.entity.user_entity import Role
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import UnauthorizedRoleError


@dataclass
class ListUsersRequestInput:
    actor_id: int
    actor_role: Role
    page: int = 1
    size: int = 20
    username: Optional[str] = None


@dataclass
class ListUsersItemData:
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    update_at: datetime


@dataclass
class ListUsersResponseOutput:
    items: List[ListUsersItemData]
    total: int
    page: int
    size: int


class ListUsersUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, request: ListUsersRequestInput) -> ListUsersResponseOutput:
        if request.actor_role not in (Role.SuperAdmin, Role.Admin):
            raise UnauthorizedRoleError("فقط سوپرادمین‌ها و مدیران می‌توانند کاربران را لیست کنند.")

        users, total = self.user_repository.find_all_paginated(request.page, request.size, request.username)

        items = [
            ListUsersItemData(
                id=u.id,
                first_name=u.first_name,
                last_name=u.last_name,
                username=u.username,
                email=u.email,
                role=u.role.value,
                is_active=u.is_active,
                created_at=u.created_at,
                update_at=u.update_at,
            )
            for u in users
        ]

        return ListUsersResponseOutput(
            items=items,
            total=total,
            page=request.page,
            size=request.size,
        )
