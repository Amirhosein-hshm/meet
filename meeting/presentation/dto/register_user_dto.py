
from pydantic import BaseModel, EmailStr
from domain.entity.user_entity import Role

class RegisterRequestDTO(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    role: Role

class RegisterResponseDTO(BaseModel):
    id: int
    email: str
    username: str
    role: str
    is_active: bool
    message: str