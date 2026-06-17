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
            raise UnauthorizedRoleError("Authenticated user not found.")

        target = self.user_repository.find_by_id(request.target_user_id)
        if not target:
            raise ResourceNotFoundError(f"User with id '{request.target_user_id}' not found.")

        if request.actor_role == Role.SuperAdmin:
            if target.id == request.actor_id:
                raise RoleHierarchyViolationError(
                    "SuperAdmin cannot delete themselves."
                )

        elif request.actor_role == Role.Admin:
            if target.role in (Role.Admin, Role.SuperAdmin):
                raise RoleHierarchyViolationError("Admins cannot delete other Admins or the SuperAdmin.")
            if target.id == request.actor_id:
                raise RoleHierarchyViolationError("Admins cannot delete themselves.")

        else:
            raise UnauthorizedRoleError("You do not have permission to delete users.")

        self.user_repository.delete(request.target_user_id)

        return DeleteUserResponseOutput(user_id=request.target_user_id)
