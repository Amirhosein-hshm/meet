from pydantic import BaseModel, EmailStr
from domain.entity.user_entity import Role

class LoginRequestDTO(BaseModel):
    username: str 
    password: str

class LoginResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    message: str
