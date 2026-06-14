from typing import List, Optional
from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class ListMeetsQueryDTO(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Items per page")
    start_date: Optional[datetime] = Field(default=None, description="Filter by start_time >= this date")
    end_date: Optional[datetime] = Field(default=None, description="Filter by start_time <= this date")
    guest_username: Optional[str] = Field(default=None, description="Filter by participant username")
    title_query: Optional[str] = Field(default=None, min_length=1, description="Search by title")


class UpdateMeetRequestDTO(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=255, description="Meeting title")
    start_time: Optional[datetime] = Field(default=None, description="Meeting start time")
    expires_at: Optional[datetime] = Field(default=None, description="Meeting expiration time")
    guest_usernames: Optional[List[str]] = Field(default=None, min_length=1, description="Replace participant list")
    assign_to_username: Optional[str] = Field(default=None, description="Reassign creator (Admin/SuperAdmin only)")

    @model_validator(mode="after")
    def validate_times(self):
        if self.start_time is not None and self.expires_at is not None:
            if self.expires_at <= self.start_time:
                raise ValueError("expires_at must be after start_time")
        return self


class MeetDetailData(BaseModel):
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


class MeetListItemData(BaseModel):
    id: int
    title: str
    meet_hash: str
    start_time: datetime
    expires_at: datetime
    creator_id: int
    is_active: bool
    participant_count: int


class PaginatedUserMeetsQueryDTO(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Items per page")
