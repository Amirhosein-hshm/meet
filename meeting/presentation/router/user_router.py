from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from domain.entity.user_entity import User
from application.usecases.get_user_usecase import GetMeRequestInput, GetMeUseCase
from application.usecases.login_user_usecase import LoginRequestInput, LoginUseCase
from application.usecases.logout_user_usecase import LogoutRequestInput, LogoutUseCase
from application.usecases.refresh_token_usecase import RefreshTokenRequestInput, RefreshTokenUseCase
from application.usecases.register_user_usecase import RegisterUserRequestInput, RegisterUserUseCase
from application.usecases.list_user_invitations_usecase import ListUserInvitationsRequestInput, ListUserInvitationsUseCase
from application.usecases.list_user_managed_meets_usecase import ListUserManagedMeetsRequestInput, ListUserManagedMeetsUseCase
from presentation.dto.refresh_token_dto import RefreshTokenRequestDTO
from presentation.dto.register_user_dto import RegisterRequestDTO
from presentation.dto.meet_dto import PaginatedUserMeetsQueryDTO, MeetListItemData
from presentation.dto.base_dto import MutationResponseDTO, PaginatedResponseDTO
from presentation.dto.register_user_dto import RegisterResponseDTO
from presentation.dto.login_user_dto import LoginResponseDTO
from presentation.dto.get_user_dto import GetMeResponseDTO
from presentation.dto.refresh_token_dto import RefreshTokenResponseDTO
from presentation.presenter.user_presenter import UserPresenter
from presentation.presenter.meet_presenter import MeetPresenter
from presentation.dependencies.auth_stub import get_current_user_stub


router = APIRouter(prefix="/users", tags=["Users"])


def get_register_use_case_stub() -> RegisterUserUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


@router.post("/register", response_model=MutationResponseDTO[RegisterResponseDTO])
def register_user(

    request: RegisterRequestDTO,
    use_case: RegisterUserUseCase = Depends(get_register_use_case_stub),
):
    dto_request = RegisterUserRequestInput(
        first_name=request.first_name,
        last_name=request.last_name,
        username=request.username,
        email=request.email,
        password=request.password,
        role=request.role,
    )
    dto_response = use_case.execute(dto_request)
    return UserPresenter.format_register_response(dto_response)


def get_login_use_case_stub() -> LoginUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


@router.post("/login", response_model=LoginResponseDTO)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: LoginUseCase = Depends(get_login_use_case_stub),
):
    dto_request = LoginRequestInput(
        username=form_data.username,
        password=form_data.password,
    )
    dto_response = use_case.execute(dto_request)

    return UserPresenter.format_login_response(dto_response)


def get_me_use_case_stub() -> GetMeUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


@router.get("/me", response_model=MutationResponseDTO[GetMeResponseDTO])
def get_current_user_profile(
    current_user: User = Depends(get_current_user_stub),
    use_case: GetMeUseCase = Depends(get_me_use_case_stub),
):
    dto_request = GetMeRequestInput(user_id=current_user.id)
    dto_response = use_case.execute(dto_request)
    return UserPresenter.format_me_response(dto_response)


def get_refresh_token_use_case_stub() -> RefreshTokenUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


@router.post("/refresh", response_model=RefreshTokenResponseDTO)
def refresh_token(
    request: RefreshTokenRequestDTO,
    use_case: RefreshTokenUseCase = Depends(get_refresh_token_use_case_stub),
):
    dto_request = RefreshTokenRequestInput(refresh_token=request.refresh_token)
    dto_response = use_case.execute(dto_request)
    return dto_response


def get_logout_use_case_stub() -> LogoutUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


@router.post("/logout")
def logout_user(
    request: RefreshTokenRequestDTO,
    current_user: User = Depends(get_current_user_stub),
    use_case: LogoutUseCase = Depends(get_logout_use_case_stub),
):
    dto_request = LogoutRequestInput(user_id=current_user.id, refresh_token=request.refresh_token)
    use_case.execute(dto_request)
    return {"detail": "Successfully logged out"}


def get_user_invitations_use_case_stub() -> ListUserInvitationsUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


@router.get("/me/invitations", response_model=PaginatedResponseDTO[MeetListItemData])
def get_user_invitations(
    query: PaginatedUserMeetsQueryDTO = Depends(),
    current_user: User = Depends(get_current_user_stub),
    use_case: ListUserInvitationsUseCase = Depends(get_user_invitations_use_case_stub),
):
    dto_request = ListUserInvitationsRequestInput(
        actor_id=current_user.id,
        actor_role=current_user.role,
        page=query.page,
        size=query.size,
    )
    dto_response = use_case.execute(dto_request)
    return MeetPresenter.format_invitations_response(dto_response)


def get_user_managed_meets_use_case_stub() -> ListUserManagedMeetsUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


@router.get("/me/managed-meets", response_model=PaginatedResponseDTO[MeetListItemData])
def get_user_managed_meets(
    query: PaginatedUserMeetsQueryDTO = Depends(),
    current_user: User = Depends(get_current_user_stub),
    use_case: ListUserManagedMeetsUseCase = Depends(get_user_managed_meets_use_case_stub),
):
    dto_request = ListUserManagedMeetsRequestInput(
        actor_id=current_user.id,
        actor_role=current_user.role,
        page=query.page,
        size=query.size,
    )
    dto_response = use_case.execute(dto_request)
    return MeetPresenter.format_managed_meets_response(dto_response)
