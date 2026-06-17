from fastapi import APIRouter, Depends

from domain.entity.user_entity import User
from application.usecases.generate_livekit_token_usecase import (
    GenerateLiveKitTokenRequestInput,
    GenerateLiveKitTokenUseCase,
)
from presentation.dto.base_dto import MutationResponseDTO
from presentation.dto.livekit_dto import LiveKitTokenData
from presentation.presenter.livekit_presenter import LiveKitPresenter
from presentation.dependencies.auth_stub import get_current_user_stub


router = APIRouter(prefix="/meets", tags=["LiveKit"])


def generate_livekit_token_use_case_stub() -> GenerateLiveKitTokenUseCase:
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
