from dataclasses import dataclass
from datetime import datetime
from typing import List

from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository
from domain.exceptions.base_exceptions import ResourceNotFoundError, ForbiddenActionError


@dataclass
class GetMeetByHashRequestInput:
    meet_hash: str
    actor_id: int
    actor_role: Role


@dataclass
class GetMeetByHashResponseOutput:
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


class GetMeetByHashUseCase:
    def __init__(self, meet_repository: IMeetRepository):
        self.meet_repository = meet_repository

    def execute(self, request: GetMeetByHashRequestInput) -> GetMeetByHashResponseOutput:
        meet = self.meet_repository.find_by_hash(request.meet_hash)
        if not meet:
            raise ResourceNotFoundError(f"Meeting with hash '{request.meet_hash}' not found.")

        if request.actor_role not in (Role.SuperAdmin, Role.Admin):
            can_access = (
                request.actor_role == Role.Host
                and (meet.creator_id == request.actor_id or request.actor_id in meet.participants_ids)
            ) or (
                request.actor_role == Role.User
                and request.actor_id in meet.participants_ids
            )
            if not can_access:
                raise ForbiddenActionError("You do not have access to this meeting.")

        return GetMeetByHashResponseOutput(
            id=meet.id,
            title=meet.title,
            meet_hash=meet.meet_hash,
            start_time=meet.start_time,
            expires_at=meet.expires_at,
            creator_id=meet.creator_id,
            is_active=meet.is_active,
            participant_ids=meet.participants_ids,
            created_at=meet.created_at,
            updated_at=meet.update_at,
        )
