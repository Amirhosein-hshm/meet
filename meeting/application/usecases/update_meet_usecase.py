from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from domain.entity.meet_entity import Meet
from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import (
    ResourceNotFoundError,
    UnauthorizedRoleError,
    RoleHierarchyViolationError,
    InvalidParticipantError,
)


@dataclass
class UpdateMeetRequestInput:
    meet_hash: str
    actor_id: int
    actor_role: Role
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    guest_usernames: Optional[List[str]] = None
    assign_to_username: Optional[str] = None


@dataclass
class UpdateMeetResponseOutput:
    id: int
    title: str
    meet_hash: str
    start_time: datetime
    expires_at: datetime
    creator_id: int
    is_active: bool
    participant_ids: List[int]
    created_at: datetime
    updated_at: datetime


class UpdateMeetUseCase:
    def __init__(self, meet_repository: IMeetRepository, user_repository: IUserRepository):
        self.meet_repository = meet_repository
        self.user_repository = user_repository

    def execute(self, request: UpdateMeetRequestInput) -> UpdateMeetResponseOutput:
        meet = self.meet_repository.find_by_hash(request.meet_hash)
        if not meet:
            raise ResourceNotFoundError(f"Meeting with hash '{request.meet_hash}' not found.")

        actor = self.user_repository.find_by_id(request.actor_id)
        if not actor:
            raise UnauthorizedRoleError("Authenticated user not found.")

        current_creator = self.user_repository.find_by_id(meet.creator_id)
        target_creator = current_creator

        if request.assign_to_username:
            target_user = self.user_repository.find_by_username(request.assign_to_username)
            if not target_user:
                raise InvalidParticipantError(f"Target creator '{request.assign_to_username}' not found.")
            if target_user.role not in [Role.Host, Role.Admin, Role.SuperAdmin]:
                raise InvalidParticipantError("Target creator must have a role of Host, Admin, or SuperAdmin.")
            target_creator = target_user

        is_reassigning = target_creator.id != meet.creator_id if request.assign_to_username else False

        if request.actor_role == Role.Host:
            if meet.creator_id != request.actor_id:
                raise RoleHierarchyViolationError("Hosts can only update their own meetings.")
            if is_reassigning:
                raise RoleHierarchyViolationError("Hosts cannot reassign meetings.")

        elif request.actor_role == Role.Admin:
            if current_creator and current_creator.role in (Role.Admin, Role.SuperAdmin) and current_creator.id != request.actor_id:
                raise RoleHierarchyViolationError("Admins cannot modify meetings created by other Admins or the SuperAdmin.")
            if is_reassigning and target_creator.role != Role.Host:
                raise RoleHierarchyViolationError("Admins can only reassign meetings to Hosts.")

        elif request.actor_role == Role.SuperAdmin:
            pass

        else:
            raise UnauthorizedRoleError("You do not have permission to update meetings.")

        if request.title is not None:
            meet.title = request.title
        if request.start_time is not None:
            meet.start_time = request.start_time
        if request.expires_at is not None:
            meet.expires_at = request.expires_at
        if request.guest_usernames is not None:
            new_participant_ids = []
            for username in request.guest_usernames:
                guest = self.user_repository.find_by_username(username)
                if guest and guest.id != target_creator.id:
                    new_participant_ids.append(guest.id)
            if not new_participant_ids:
                raise InvalidParticipantError("At least one valid guest username must be provided.")
            meet.participants_ids = new_participant_ids
        if is_reassigning:
            meet.creator_id = target_creator.id

        if request.expires_at is not None or request.start_time is not None:
            meet.update_at = datetime.utcnow()

        saved_meet = self.meet_repository.save(meet)

        return UpdateMeetResponseOutput(
            id=saved_meet.id,
            title=saved_meet.title,
            meet_hash=saved_meet.meet_hash,
            start_time=saved_meet.start_time,
            expires_at=saved_meet.expires_at,
            creator_id=saved_meet.creator_id,
            is_active=saved_meet.is_active,
            participant_ids=saved_meet.participants_ids,
            created_at=saved_meet.created_at,
            updated_at=saved_meet.update_at,
        )
