from application.usecases.get_user_usecase import GetMeResponseOutput
from application.usecases.login_user_usecase import LoginResponseOutput
from application.usecases.register_user_usecase import RegisterUserResponseOutput
from application.usecases.list_users_usecase import ListUsersResponseOutput, ListUsersItemData
from application.usecases.delete_user_usecase import DeleteUserResponseOutput
from application.usecases.update_user_usecase import UpdateUserResponseOutput
from application.usecases.get_user_by_username_usecase import GetUserByUsernameResponseOutput
from presentation.dto.login_user_dto import LoginResponseDTO
from presentation.dto.register_user_dto import RegisterResponseDTO
from presentation.dto.get_user_dto import GetMeResponseDTO
from presentation.dto.base_dto import MutationResponseDTO, SingleResponseDTO, PaginatedResponseDTO


class UserPresenter:
    @staticmethod
    def format_register_response(dto: RegisterUserResponseOutput) -> MutationResponseDTO:
        return MutationResponseDTO(
            data=dto,
            message="ثبت نام با موفقیت انجام شد.",
        )

    @staticmethod
    def format_login_response(dto: LoginResponseOutput) -> LoginResponseDTO:
        return LoginResponseDTO(
            access_token=dto.access_token,
            refresh_token=dto.refresh_token,
            token_type="bearer",
            message="ورود با موفقیت انجام شد.",
        )

    @staticmethod
    def format_me_response(dto: GetMeResponseOutput) -> MutationResponseDTO:
        return MutationResponseDTO(
            data=dto,
            message="پروفایل کاربر با موفقیت دریافت شد.",
        )

    @staticmethod
    def format_list_users_response(dto: ListUsersResponseOutput) -> PaginatedResponseDTO[GetMeResponseDTO]:
        items = [
            GetMeResponseDTO(
                id=item.id,
                first_name=item.first_name,
                last_name=item.last_name,
                username=item.username,
                email=item.email,
                role=item.role,
                is_active=item.is_active,
                created_at=item.created_at,
                update_at=item.update_at,
            )
            for item in dto.items
        ]
        total_pages = max(1, (dto.total + dto.size - 1) // dto.size)
        return PaginatedResponseDTO(
            data=items,
            total=dto.total,
            current_page=dto.page,
            pages=total_pages,
            is_next=dto.page < total_pages,
            is_prev=dto.page > 1,
            size=dto.size,
            permissions=[],
        )

    @staticmethod
    def format_delete_user_response(dto: DeleteUserResponseOutput) -> MutationResponseDTO:
        return MutationResponseDTO(
            data={"user_id": dto.user_id},
            message="کاربر با موفقیت حذف شد.",
        )

    @staticmethod
    def format_update_user_response(dto: UpdateUserResponseOutput) -> MutationResponseDTO[GetMeResponseDTO]:
        data = GetMeResponseDTO(
            id=dto.id,
            first_name=dto.first_name,
            last_name=dto.last_name,
            username=dto.username,
            email=dto.email,
            role=dto.role,
            is_active=dto.is_active,
            created_at=dto.created_at,
            update_at=dto.update_at,
        )
        return MutationResponseDTO(
            data=data,
            message="کاربر با موفقیت به‌روزرسانی شد.",
        )

    @staticmethod
    def format_get_user_by_username_response(dto: GetUserByUsernameResponseOutput) -> SingleResponseDTO[GetMeResponseDTO]:
        data = GetMeResponseDTO(
            id=dto.id,
            first_name=dto.first_name,
            last_name=dto.last_name,
            username=dto.username,
            email=dto.email,
            role=dto.role,
            is_active=dto.is_active,
            created_at=dto.created_at,
            update_at=dto.update_at,
        )
        return SingleResponseDTO(
            data=data,
            permissions=[],
        )
