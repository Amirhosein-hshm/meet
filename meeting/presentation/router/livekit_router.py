from fastapi import APIRouter, Depends

from domain.entity.user_entity import User
from application.usecases.generate_livekit_token_usecase import (
    GenerateLiveKitTokenRequestInput,
    GenerateLiveKitTokenUseCase,
)
from application.usecases.ban_participant_usecase import (
    BanParticipantRequestInput,
    BanParticipantUseCase,
)
from presentation.dto.base_dto import MutationResponseDTO
from presentation.dto.livekit_dto import LiveKitTokenData, BanParticipantResponseData
from presentation.presenter.livekit_presenter import LiveKitPresenter
from presentation.dependencies.auth_stub import get_current_user_stub


router = APIRouter(prefix="/meets", tags=["LiveKit"])


def generate_livekit_token_use_case_stub() -> GenerateLiveKitTokenUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


def ban_participant_use_case_stub() -> BanParticipantUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


@router.post("/{meet_hash}/token", response_model=MutationResponseDTO[LiveKitTokenData])
def generate_token(
    meet_hash: str,
    current_user: User = Depends(get_current_user_stub),
    use_case: GenerateLiveKitTokenUseCase = Depends(generate_livekit_token_use_case_stub),
):
    dto_request = GenerateLiveKitTokenRequestInput(
        meet_hash=meet_hash,
        actor_id=current_user.id,
        actor_role=current_user.role,
    )
    dto_response = use_case.execute(dto_request)
    return LiveKitPresenter.format_token_response(dto_response)


@router.post("/{meet_hash}/ban/{user_id}", response_model=MutationResponseDTO[BanParticipantResponseData])
def ban_participant(
    meet_hash: str,
    user_id: int,
    current_user: User = Depends(get_current_user_stub),
    use_case: BanParticipantUseCase = Depends(ban_participant_use_case_stub),
):
    dto_request = BanParticipantRequestInput(
        meet_hash=meet_hash,
        actor_id=current_user.id,
        actor_role=current_user.role,
        target_user_id=user_id,
    )
    dto_response = use_case.execute(dto_request)
    return LiveKitPresenter.format_ban_response(dto_response)
