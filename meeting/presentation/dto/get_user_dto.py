from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime

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

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if not any([self.first_name, self.last_name, self.username, self.email]):
            raise ValueError("At least one field must be provided for update")
        return self
