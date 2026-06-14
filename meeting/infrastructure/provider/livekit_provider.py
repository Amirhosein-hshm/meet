from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session

from application.usecases.generate_livekit_token_usecase import GenerateLiveKitTokenUseCase
from application.usecases.ban_participant_usecase import BanParticipantUseCase
from infrastructure.database import get_db_session
from infrastructure.repository.postgres_meet_repository import PostgresMeetRepository
from infrastructure.repository.postgres_participant_repository import PostgresParticipantRepository
from infrastructure.repository.postgres_user_repository import PostgresUserRepository
from infrastructure.livekit_service import LiveKitService
from presentation.router.livekit_router import (
    generate_livekit_token_use_case_stub,
    ban_participant_use_case_stub,
)


def create_real_generate_livekit_token_use_case(db: Session = Depends(get_db_session)):
    meet_repository = PostgresMeetRepository(db)
    participant_repository = PostgresParticipantRepository(db)
    livekit_service = LiveKitService()
    return GenerateLiveKitTokenUseCase(meet_repository, participant_repository, livekit_service)


def create_real_ban_participant_use_case(db: Session = Depends(get_db_session)):
    meet_repository = PostgresMeetRepository(db)
    participant_repository = PostgresParticipantRepository(db)
    user_repository = PostgresUserRepository(db)
    livekit_service = LiveKitService()
    return BanParticipantUseCase(meet_repository, participant_repository, user_repository, livekit_service)


def register_livekit_di(app: FastAPI):
    app.dependency_overrides[generate_livekit_token_use_case_stub] = create_real_generate_livekit_token_use_case
    app.dependency_overrides[ban_participant_use_case_stub] = create_real_ban_participant_use_case
