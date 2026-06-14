from pydantic.dataclasses import dataclass
from application.usecases.login_user_usecase import ITokenService
from domain.repository_interface.refresh_token_repository_interface import IRefreshTokenRepository
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import ResourceNotFoundError, ForbiddenActionError


@dataclass
class RefreshTokenRequestInput:
    refresh_token: str
@dataclass
class RefreshTokenResponseOutput:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"




class RefreshTokenUseCase:
    def __init__(self, refresh_token_repository: IRefreshTokenRepository, user_repository: IUserRepository, token_service: ITokenService):
        self.refresh_token_repository = refresh_token_repository
        self.user_repository = user_repository
        self.token_service = token_service

    def execute(self, input_data: RefreshTokenRequestInput) -> RefreshTokenResponseOutput:
        try:
            payload = self.token_service.decode_token(input_data.refresh_token)
            if payload.get("type") != "refresh":
                raise ForbiddenActionError("Invalid token type")

            user_id = int(payload.get("sub"))
        except Exception as e:
            raise ForbiddenActionError("Invalid or expired refresh token")

        if not self.refresh_token_repository.is_valid(user_id, input_data.refresh_token):
            raise ForbiddenActionError("Refresh token has been revoked")

        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ResourceNotFoundError("User not found")
        
        self.refresh_token_repository.revoke(user_id, input_data.refresh_token)

        access_payload = {"sub": str(user.id), "username": user.username, "role": user.role.value, "type": "access" }
        new_access = self.token_service.generate_access_token(access_payload)

        refresh_payload = {"sub": str(user.id), "username": user.username, "role": user.role.value, "type": "refresh"}
        new_refresh = self.token_service.generate_refresh_token(refresh_payload)

        self.refresh_token_repository.save(user_id, new_refresh)

        return RefreshTokenResponseOutput(access_token=new_access, refresh_token=new_refresh)