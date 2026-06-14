from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session

from application.usecases.create_meet_usecase import CreateMeetUseCase
from application.usecases.get_meet_by_hash_usecase import GetMeetByHashUseCase
from application.usecases.list_meets_usecase import ListMeetsUseCase
from application.usecases.update_meet_usecase import UpdateMeetUseCase
from application.usecases.delete_meet_usecase import DeleteMeetUseCase
from infrastructure.database import get_db_session
from infrastructure.repository.postgres_meet_repository import PostgresMeetRepository
from infrastructure.repository.postgres_user_repository import PostgresUserRepository
from infrastructure.auth_guard import get_real_current_user
from presentation.dependencies.auth_stub import get_current_user_stub
from presentation.router.meet_router import (
    create_meet_use_case_stub,
    get_meet_by_hash_use_case_stub,
    list_meets_use_case_stub,
    update_meet_use_case_stub,
    delete_meet_use_case_stub,
)


def create_real_meet_use_case(db: Session = Depends(get_db_session)):
    meet_repository = PostgresMeetRepository(db)
    user_repository = PostgresUserRepository(db)
    return CreateMeetUseCase(meet_repository, user_repository)


def create_real_get_meet_by_hash_use_case(db: Session = Depends(get_db_session)):
    meet_repository = PostgresMeetRepository(db)
    return GetMeetByHashUseCase(meet_repository)


def create_real_list_meets_use_case(db: Session = Depends(get_db_session)):
    meet_repository = PostgresMeetRepository(db)
    return ListMeetsUseCase(meet_repository)


def create_real_update_meet_use_case(db: Session = Depends(get_db_session)):
    meet_repository = PostgresMeetRepository(db)
    user_repository = PostgresUserRepository(db)
    return UpdateMeetUseCase(meet_repository, user_repository)


def create_real_delete_meet_use_case(db: Session = Depends(get_db_session)):
    meet_repository = PostgresMeetRepository(db)
    user_repository = PostgresUserRepository(db)
    return DeleteMeetUseCase(meet_repository, user_repository)


def register_meet_di(app: FastAPI):
    app.dependency_overrides[create_meet_use_case_stub] = create_real_meet_use_case
    app.dependency_overrides[get_meet_by_hash_use_case_stub] = create_real_get_meet_by_hash_use_case
    app.dependency_overrides[list_meets_use_case_stub] = create_real_list_meets_use_case
    app.dependency_overrides[update_meet_use_case_stub] = create_real_update_meet_use_case
    app.dependency_overrides[delete_meet_use_case_stub] = create_real_delete_meet_use_case
    app.dependency_overrides[get_current_user_stub] = get_real_current_user
