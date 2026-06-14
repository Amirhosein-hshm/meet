# presentation/dto/create_meet_dto.py
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator
from datetime import datetime

class CreateMeetRequestDTO(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, description="Meeting title")
    start_time: datetime = Field(..., description="Meeting start time")
    expires_at: datetime = Field(..., description="Meeting expiration time")
    guest_usernames: List[str] = Field(..., min_length=1, description="List of guest usernames to invite")
    assign_to_username: Optional[str] = Field(default=None, description="Optional: Username to assign as creator (Admin/SuperAdmin only)")

    @model_validator(mode="after")
    def validate_times(self):
        if self.expires_at <= self.start_time:
            raise ValueError("expires_at must be after start_time")
        return self


class MeetResponseData(BaseModel):
    id: int
    title: str
    meet_hash: str
    start_time: datetime
    expires_at: datetime
    creator_id: int