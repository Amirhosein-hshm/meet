from dataclasses import dataclass

from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import (
    ResourceNotFoundError,
    UnauthorizedRoleError,
    RoleHierarchyViolationError,
)


@dataclass
class DeleteMeetRequestInput:
    meet_hash: str
    actor_id: int
    actor_role: Role


@dataclass
class DeleteMeetResponseOutput:
    meet_hash: str


class DeleteMeetUseCase:
    def __init__(self, meet_repository: IMeetRepository, user_repository: IUserRepository):
        self.meet_repository = meet_repository
        self.user_repository = user_repository

    def execute(self, request: DeleteMeetRequestInput) -> DeleteMeetResponseOutput:
        meet = self.meet_repository.find_by_hash(request.meet_hash)
        if not meet:
            raise ResourceNotFoundError(f"جلسه با هش '{request.meet_hash}' یافت نشد.")

        actor = self.user_repository.find_by_id(request.actor_id)
        if not actor:
            raise UnauthorizedRoleError("کاربر احراز هویت شده یافت نشد.")

        current_creator = self.user_repository.find_by_id(meet.creator_id)

        if request.actor_role == Role.Host:
            if meet.creator_id != request.actor_id:
                raise RoleHierarchyViolationError("میزبان‌ها فقط می‌توانند جلسات خود را حذف کنند.")

        elif request.actor_role == Role.Admin:
            if current_creator and current_creator.role in (Role.Admin, Role.SuperAdmin) and current_creator.id != request.actor_id:
                raise RoleHierarchyViolationError("مدیران نمی‌توانند جلسات ایجاد شده توسط مدیران دیگر یا سوپرادمین را حذف کنند.")

        elif request.actor_role == Role.SuperAdmin:
            pass

        else:
            raise UnauthorizedRoleError("شما مجوز حذف جلسات را ندارید.")

        self.meet_repository.delete(meet.id)

        return DeleteMeetResponseOutput(meet_hash=request.meet_hash)
