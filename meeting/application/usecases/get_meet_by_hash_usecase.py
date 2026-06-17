from dataclasses import dataclass
from datetime import datetime
from typing import List

from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import ResourceNotFoundError, ForbiddenActionError


@dataclass
class GetMeetByHashRequestInput:
    meet_hash: str
    actor_id: int
    actor_role: Role


@dataclass
class ParticipantUserData:
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class GetMeetByHashResponseOutput:
    id: int
    title: str
    meet_hash: str
    start_time: datetime
    expires_at: datetime
    creator_id: int
    is_active: bool
    participants: List[ParticipantUserData]
    created_at: datetime
    updated_at: datetime


class GetMeetByHashUseCase:
    def __init__(self, meet_repository: IMeetRepository, user_repository: IUserRepository):
        self.meet_repository = meet_repository
        self.user_repository = user_repository

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

        users = self.user_repository.find_by_ids(meet.participants_ids)
        user_map = {u.id: u for u in users}

        ordered_participants = []
        for pid in meet.participants_ids:
            user = user_map.get(pid)
            if user is not None:
                ordered_participants.append(
                    ParticipantUserData(
                        id=user.id,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        username=user.username,
                        email=user.email,
                        role=user.role.value,
                        is_active=user.is_active,
                        created_at=user.created_at,
                        updated_at=user.update_at,
                    )
                )

        return GetMeetByHashResponseOutput(
            id=meet.id,
            title=meet.title,
            meet_hash=meet.meet_hash,
            start_time=meet.start_time,
            expires_at=meet.expires_at,
            creator_id=meet.creator_id,
            is_active=meet.is_active,
            participants=ordered_participants,
            created_at=meet.created_at,
            updated_at=meet.update_at,
        )
