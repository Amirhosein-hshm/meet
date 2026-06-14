
from pydantic import BaseModel


class RefreshTokenRequestDTO(BaseModel):
    refresh_token: str


class RefreshTokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"