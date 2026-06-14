from dataclasses import dataclass

from domain.repository_interface.refresh_token_repository_interface import IRefreshTokenRepository

@dataclass
class LogoutRequestInput:
        user_id: int 
        refresh_token :str

class LogoutUseCase:
    def __init__(self, refresh_token_repository: IRefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository

    def execute(self, input_data: LogoutRequestInput) -> bool:
        self.refresh_token_repository.revoke(input_data.user_id, input_data.refresh_token)
        return True