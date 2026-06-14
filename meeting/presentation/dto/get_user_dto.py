from pydantic import BaseModel, EmailStr
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
    created_at: datetime
    update_at: datetime
