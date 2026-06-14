from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entity.user_entity import User
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.entity.user_entity import Role
from domain.exceptions.base_exceptions import ConflictError

class IPasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass


@dataclass
class RegisterUserRequestInput:
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    role: Role

@dataclass
class RegisterUserResponseOutput:
    id: int
    email: str
    username: str
    role: str
    is_active: bool



class RegisterUserUseCase:
    def __init__(self, user_repository: IUserRepository, password_hasher: IPasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, request: RegisterUserRequestInput) -> RegisterUserResponseOutput:
        # 1. Check if user exists
        existing_user = self.user_repository.find_by_username(request.username)
        if existing_user:
            raise ConflictError("Username already in use")

        # 2. Hash password
        hashed_password = self.password_hasher.hash_password(request.password)

        # 3. Create Entity
        new_user = User(
            first_name=request.first_name,
            last_name=request.last_name,
            username=request.username,
            email=request.email,
            password_hash=hashed_password,
            role=request.role
        )

        # 4. Save to DB
        saved_user = self.user_repository.save(new_user)

        # 5. Return Output DTO
        return RegisterUserResponseOutput(
            id=saved_user.id,
            email=saved_user.email,
            role=saved_user.role.value,
            is_active=saved_user.is_active,
            username=saved_user.username
        )