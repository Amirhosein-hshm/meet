from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository, MeetFilter
from domain.exceptions.base_exceptions import ForbiddenActionError


@dataclass
class ListMeetsRequestInput:
    actor_id: int
    actor_role: Role
    page: int = 1
    size: int = 20
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    guest_username: Optional[str] = None
    title_query: Optional[str] = None


@dataclass
class ListMeetsItemData:
    id: int
    title: str
    meet_hash: str
    start_time: datetime
    expires_at: datetime
    creator_id: int
    is_active: bool
    participant_count: int


@dataclass
class ListMeetsResponseOutput:
    items: List[ListMeetsItemData]
    total: int
    page: int
    size: int


class ListMeetsUseCase:
    def __init__(self, meet_repository: IMeetRepository):
        self.meet_repository = meet_repository

    def execute(self, request: ListMeetsRequestInput) -> ListMeetsResponseOutput:
        filters = MeetFilter(
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            start_date_from=request.start_date,
            start_date_to=request.end_date,
            guest_username=request.guest_username,
            title_query=request.title_query,
        )

        meets, total = self.meet_repository.find_paginated(filters, request.page, request.size)

        total_pages = max(1, (total + request.size - 1) // request.size)

        items = [
            ListMeetsItemData(
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

        return ListMeetsResponseOutput(
            items=items,
            total=total,
            page=request.page,
            size=request.size,
        )
