from dataclasses import dataclass
from datetime import datetime
from typing import List

from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository, MeetFilter
from domain.exceptions.base_exceptions import UnauthorizedRoleError


@dataclass
class ListUserManagedMeetsRequestInput:
    actor_id: int
    actor_role: Role
    page: int = 1
    size: int = 20


@dataclass
class ListUserManagedMeetsItemData:
    id: int
    title: str
    meet_hash: str
    start_time: datetime
    expires_at: datetime
    creator_id: int
    is_active: bool
    participant_count: int


@dataclass
class ListUserManagedMeetsResponseOutput:
    items: List[ListUserManagedMeetsItemData]
    total: int
    page: int
    size: int


class ListUserManagedMeetsUseCase:
    def __init__(self, meet_repository: IMeetRepository):
        self.meet_repository = meet_repository

    def execute(self, request: ListUserManagedMeetsRequestInput) -> ListUserManagedMeetsResponseOutput:
        filters = MeetFilter(
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            creator_id=request.actor_id,
        )

        meets, total = self.meet_repository.find_paginated(filters, request.page, request.size)

        items = [
            ListUserManagedMeetsItemData(
                id=m.id,
                title=m.title,
                meet_hash=m.meet_hash,
                start_time=m.start_time,
                expires_at=m.expires_at,
                creator_id=m.creator_id,
                is_active=m.is_active,
                participant_count=len(m.participants_ids),
            )
            for m in meets
        ]

        return ListUserManagedMeetsResponseOutput(
            items=items,
            total=total,
            page=request.page,
            size=request.size,
        )
