from dataclasses import dataclass
from pydantic import BaseModel, EmailStr
from datetime import datetime
from domain.entity.user_entity import Role
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import ResourceNotFoundError

@dataclass
class GetMeRequestInput:
    user_id: int
@dataclass
class GetMeResponseOutput:
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    role: Role 
    created_at: datetime
    update_at: datetime

class GetMeUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, request: GetMeRequestInput) -> GetMeResponseOutput:
        user = self.user_repository.find_by_id(request.user_id)
        if not user:
            raise ResourceNotFoundError("User not found.")
        return GetMeResponseOutput(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            update_at=user.update_at
        )