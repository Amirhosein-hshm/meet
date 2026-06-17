from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.entity.user_entity import Role, User
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import (
    ResourceNotFoundError,
    UnauthorizedRoleError,
    RoleHierarchyViolationError,
    ConflictError,
)


@dataclass
class UpdateUserRequestInput:
    actor_id: int
    actor_role: Role
    target_user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None


@dataclass
class UpdateUserResponseOutput:
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    update_at: datetime


class UpdateUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, request: UpdateUserRequestInput) -> UpdateUserResponseOutput:
        actor = self.user_repository.find_by_id(request.actor_id)
        if not actor:
            raise UnauthorizedRoleError("Authenticated user not found.")

        target = self.user_repository.find_by_id(request.target_user_id)
        if not target:
            raise ResourceNotFoundError(f"User with id '{request.target_user_id}' not found.")

        if request.actor_role == Role.SuperAdmin:
            pass

        elif request.actor_role == Role.Admin:
            if target.id != request.actor_id and target.role in (Role.Admin, Role.SuperAdmin):
                raise RoleHierarchyViolationError("Admins cannot update other Admins or the SuperAdmin.")

        elif request.actor_role in (Role.Host, Role.User):
            if target.id != request.actor_id:
                raise RoleHierarchyViolationError("You can only update your own account.")

        else:
            raise UnauthorizedRoleError("You do not have permission to update users.")

        if request.username is not None and request.username != target.username:
            existing = self.user_repository.find_by_username(request.username)
            if existing is not None and existing.id != target.id:
                raise ConflictError("Username is already in use.")

        if request.email is not None and request.email != target.email:
            existing = self.user_repository.find_by_email(request.email)
            if existing is not None and existing.id != target.id:
                raise ConflictError("Email is already in use.")

        if request.first_name is not None:
            target.first_name = request.first_name
        if request.last_name is not None:
            target.last_name = request.last_name
        if request.username is not None:
            target.username = request.username
        if request.email is not None:
            target.email = request.email
        target.update_at = datetime.utcnow()

        saved = self.user_repository.save(target)

        return UpdateUserResponseOutput(
            id=saved.id,
            first_name=saved.first_name,
            last_name=saved.last_name,
            username=saved.username,
            email=saved.email,
            role=saved.role.value,
            is_active=saved.is_active,
            created_at=saved.created_at,
            update_at=saved.update_at,
        )
