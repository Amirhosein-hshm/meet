from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from application.usecases.get_user_usecase import GetMeUseCase
from application.usecases.login_user_usecase import LoginUseCase
from application.usecases.logout_user_usecase import LogoutUseCase
from application.usecases.refresh_token_usecase import RefreshTokenUseCase
from application.usecases.register_user_usecase import RegisterUserUseCase
from application.usecases.list_user_invitations_usecase import ListUserInvitationsUseCase
from application.usecases.list_user_managed_meets_usecase import ListUserManagedMeetsUseCase
from infrastructure.database import get_db_session
from infrastructure.repository.postgres_meet_repository import PostgresMeetRepository
from infrastructure.repository.postgres_refresh_token_repository import PostgresRefreshTokenRepository
from infrastructure.repository.postgres_user_repository import PostgresUserRepository
from infrastructure.security import BcryptPasswordHasher, JwtTokenService
from infrastructure.auth_guard import get_real_current_user
from presentation.dependencies.auth_stub import get_current_user_stub
from presentation.router.user_router import (
    get_register_use_case_stub,
    get_login_use_case_stub,
    get_me_use_case_stub,
    get_refresh_token_use_case_stub,
    get_logout_use_case_stub,
    get_user_invitations_use_case_stub,
    get_user_managed_meets_use_case_stub,
)


def get_real_register_use_case(db: Session = Depends(get_db_session)):
    repository = PostgresUserRepository(db)
    hasher = BcryptPasswordHasher()
    return RegisterUserUseCase(repository, hasher)


def get_real_login_use_case(db: Session = Depends(get_db_session)):
    user_repo = PostgresUserRepository(db)
    refresh_token_repo = PostgresRefreshTokenRepository(db)
    password_hasher = BcryptPasswordHasher()
    token_service = JwtTokenService()
    return LoginUseCase(
        user_repository=user_repo,
        refresh_token_repository=refresh_token_repo,
        password_hasher=password_hasher,
        token_service=token_service,
    )


def get_real_me_use_case(db: Session = Depends(get_db_session)):
    user_repo = PostgresUserRepository(db)
    return GetMeUseCase(user_repository=user_repo)


def get_real_refresh_token_use_case(db: Session = Depends(get_db_session)):
    refresh_token_repo = PostgresRefreshTokenRepository(db)
    user_repo = PostgresUserRepository(db)
    token_service = JwtTokenService()
    return RefreshTokenUseCase(
        refresh_token_repository=refresh_token_repo,
        user_repository=user_repo,
        token_service=token_service,
    )


def get_real_logout_use_case(db: Session = Depends(get_db_session)):
    refresh_token_repo = PostgresRefreshTokenRepository(db)
    return LogoutUseCase(refresh_token_repository=refresh_token_repo)


def get_real_user_invitations_use_case(db: Session = Depends(get_db_session)):
    meet_repo = PostgresMeetRepository(db)
    return ListUserInvitationsUseCase(meet_repo)


def get_real_user_managed_meets_use_case(db: Session = Depends(get_db_session)):
    meet_repo = PostgresMeetRepository(db)
    return ListUserManagedMeetsUseCase(meet_repo)


def register_user_di(app: FastAPI):
    app.dependency_overrides[get_current_user_stub] = get_real_current_user
    app.dependency_overrides[get_register_use_case_stub] = get_real_register_use_case
    app.dependency_overrides[get_login_use_case_stub] = get_real_login_use_case
    app.dependency_overrides[get_me_use_case_stub] = get_real_me_use_case
    app.dependency_overrides[get_refresh_token_use_case_stub] = get_real_refresh_token_use_case
    app.dependency_overrides[get_logout_use_case_stub] = get_real_logout_use_case
    app.dependency_overrides[get_user_invitations_use_case_stub] = get_real_user_invitations_use_case
    app.dependency_overrides[get_user_managed_meets_use_case_stub] = get_real_user_managed_meets_use_case
