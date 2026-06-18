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
    role: Optional[Role] = None
    is_active: Optional[bool] = None


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


def _validate_role_active_modification(
    actor: User,
    target: User,
    new_role: Optional[Role],
    new_is_active: Optional[bool],
) -> None:
    role_changed = new_role is not None and new_role != target.role
    active_changed = new_is_active is not None and new_is_active != target.is_active

    if not role_changed and not active_changed:
        return

    if actor.role == Role.SuperAdmin:
        if new_role == Role.SuperAdmin and target.role != Role.SuperAdmin:
            raise RoleHierarchyViolationError(
                "یک سوپرادمین قبلاً وجود دارد. نمی‌توان کاربر دیگری را به سوپرادمین ارتقا داد."
            )
        return

    if actor.role == Role.Admin:
        if target.id == actor.id:
            raise RoleHierarchyViolationError(
                "مدیران نمی‌توانند نقش یا وضعیت فعال خود را تغییر دهند."
            )
        return

    if actor.role in (Role.Host, Role.User):
        raise RoleHierarchyViolationError(
            "شما مجاز به تغییر نقش یا وضعیت فعال نیستید."
        )


class UpdateUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, request: UpdateUserRequestInput) -> UpdateUserResponseOutput:
        actor = self.user_repository.find_by_id(request.actor_id)
        if not actor:
            raise UnauthorizedRoleError("کاربر احراز هویت شده یافت نشد.")

        target = self.user_repository.find_by_id(request.target_user_id)
        if not target:
            raise ResourceNotFoundError(f"کاربر با شناسه '{request.target_user_id}' یافت نشد.")

        if request.actor_role == Role.SuperAdmin:
            pass

        elif request.actor_role == Role.Admin:
            if target.id != request.actor_id and target.role in (Role.Admin, Role.SuperAdmin):
                raise RoleHierarchyViolationError("مدیران نمی‌توانند مدیران دیگر یا سوپرادمین را به‌روزرسانی کنند.")

        elif request.actor_role in (Role.Host, Role.User):
            if target.id != request.actor_id:
                raise RoleHierarchyViolationError("شما فقط می‌توانید حساب خود را به‌روزرسانی کنید.")

        else:
            raise UnauthorizedRoleError("شما مجوز به‌روزرسانی کاربران را ندارید.")

        _validate_role_active_modification(actor, target, request.role, request.is_active)

        if request.username is not None and request.username != target.username:
            existing = self.user_repository.find_by_username(request.username)
            if existing is not None and existing.id != target.id:
                raise ConflictError("نام کاربری قبلاً استفاده شده است.")

        if request.email is not None and request.email != target.email:
            existing = self.user_repository.find_by_email(request.email)
            if existing is not None and existing.id != target.id:
                raise ConflictError("ایمیل قبلاً استفاده شده است.")

        if request.first_name is not None:
            target.first_name = request.first_name
        if request.last_name is not None:
            target.last_name = request.last_name
        if request.username is not None:
            target.username = request.username
        if request.email is not None:
            target.email = request.email
        if request.role is not None:
            target.role = request.role
        if request.is_active is not None:
            target.is_active = request.is_active
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
