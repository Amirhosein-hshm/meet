from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic import EmailStr

from domain.repository_interface.refresh_token_repository_interface import IRefreshTokenRepository
from .register_user_usecase import IPasswordHasher
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import ResourceNotFoundError, ForbiddenActionError


class ITokenService(ABC):
    @abstractmethod
    def generate_access_token(self, data: dict) -> str:
        pass
    @abstractmethod
    def generate_refresh_token(self, data: dict) -> str:
        pass
    @abstractmethod
    def decode_token(self, token: str) -> dict:
        pass

@dataclass
class LoginRequestInput:
    username: str 
    password: str

@dataclass
class LoginResponseOutput:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginUseCase:
    def __init__(
        self, 
        user_repository: IUserRepository,
        refresh_token_repository: IRefreshTokenRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service
        self.refresh_token_repository = refresh_token_repository

    def execute(self, request: LoginRequestInput) -> LoginResponseOutput:
        user = self.user_repository.find_by_username(request.username)
        if not user:
            raise ResourceNotFoundError("Username not found.")

        if not self.password_hasher.verify_password(request.password, user.password_hash):
            raise ForbiddenActionError("Password is not valid.")


        access_payload = {"sub": str(user.id), "username": user.username, "role": user.role.value, "type": "access" }
        access_token = self.token_service.generate_access_token(access_payload)


        refresh_payload = {"sub": str(user.id), "username": user.username, "role": user.role.value, "type": "refresh"}
        refresh_token = self.token_service.generate_refresh_token(refresh_payload)

        self.refresh_token_repository.save(user.id, refresh_token)

        return LoginResponseOutput(access_token=access_token,
                                   refresh_token=refresh_token)