from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime

from domain.entity.user_entity import Role


class GetMeRequestDTO(BaseModel):
    user_id: int


class GetMeResponseDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    role: str
    is_active: bool = True
    created_at: datetime
    update_at: datetime


class UpdateUserRequestDTO(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(default=None)
    role: Optional[Role] = Field(default=None, description="New role")
    is_active: Optional[bool] = Field(default=None, description="Activate/deactivate user")

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if not any([
            self.first_name, self.last_name, self.username, self.email,
            self.role is not None, self.is_active is not None
        ]):
            raise ValueError("At least one field must be provided for update")
        return self


class ListUsersQueryDTO(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Items per page")
    username: Optional[str] = Field(default=None, min_length=1, description="Filter by username (case-insensitive)")
