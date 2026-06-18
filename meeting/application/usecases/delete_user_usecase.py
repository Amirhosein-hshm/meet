from dataclasses import dataclass

from domain.entity.user_entity import Role
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import (
    ResourceNotFoundError,
    UnauthorizedRoleError,
    RoleHierarchyViolationError,
)


@dataclass
class DeleteUserRequestInput:
    actor_id: int
    actor_role: Role
    target_user_id: int


@dataclass
class DeleteUserResponseOutput:
    user_id: int


class DeleteUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, request: DeleteUserRequestInput) -> DeleteUserResponseOutput:
        actor = self.user_repository.find_by_id(request.actor_id)
        if not actor:
            raise UnauthorizedRoleError("کاربر احراز هویت شده یافت نشد.")

        target = self.user_repository.find_by_id(request.target_user_id)
        if not target:
            raise ResourceNotFoundError(f"کاربر با شناسه '{request.target_user_id}' یافت نشد.")

        if request.actor_role == Role.SuperAdmin:
            if target.id == request.actor_id:
                raise RoleHierarchyViolationError(
                    "سوپرادمین نمی‌تواند خودش را حذف کند."
                )

        elif request.actor_role == Role.Admin:
            if target.role in (Role.Admin, Role.SuperAdmin):
                raise RoleHierarchyViolationError("مدیران نمی‌توانند مدیران دیگر یا سوپرادمین را حذف کنند.")
            if target.id == request.actor_id:
                raise RoleHierarchyViolationError("مدیران نمی‌توانند خودشان را حذف کنند.")

        else:
            raise UnauthorizedRoleError("شما مجوز حذف کاربران را ندارید.")

        self.user_repository.delete(request.target_user_id)

        return DeleteUserResponseOutput(user_id=request.target_user_id)
