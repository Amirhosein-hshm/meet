from application.usecases.get_user_usecase import GetMeResponseOutput
from application.usecases.login_user_usecase import LoginResponseOutput
from application.usecases.register_user_usecase import RegisterUserResponseOutput
from presentation.dto.login_user_dto import LoginResponseDTO
from presentation.dto.register_user_dto import RegisterResponseDTO
from presentation.dto.base_dto import MutationResponseDTO


class UserPresenter:
    @staticmethod
    def format_register_response(dto: RegisterUserResponseOutput) -> MutationResponseDTO:
        return MutationResponseDTO(
            data=dto,
            message="User registered successfully.",
        )

    @staticmethod
    def format_login_response(dto: LoginResponseOutput) -> LoginResponseDTO:
        return LoginResponseDTO(
            access_token=dto.access_token,
            refresh_token=dto.refresh_token,
            token_type="bearer",
            message="Login successful.",
        )

    @staticmethod
    def format_me_response(dto: GetMeResponseOutput) -> MutationResponseDTO:
        return MutationResponseDTO(
            data=dto,
            message="User profile retrieved successfully.",
        )
