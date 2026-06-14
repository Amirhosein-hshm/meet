from application.usecases.generate_livekit_token_usecase import GenerateLiveKitTokenResponseOutput
from application.usecases.ban_participant_usecase import BanParticipantResponseOutput
from presentation.dto.livekit_dto import LiveKitTokenData, BanParticipantResponseData
from presentation.dto.base_dto import MutationResponseDTO


class LiveKitPresenter:
    @staticmethod
    def format_token_response(dto: GenerateLiveKitTokenResponseOutput) -> MutationResponseDTO[LiveKitTokenData]:
        data = LiveKitTokenData(
            token=dto.token,
            room_name=dto.room_name,
        )
        return MutationResponseDTO(
            data=data,
            message="LiveKit token generated successfully.",
        )

    @staticmethod
    def format_ban_response(dto: BanParticipantResponseOutput) -> MutationResponseDTO[BanParticipantResponseData]:
        data = BanParticipantResponseData(
            meet_hash=dto.meet_hash,
            user_id=dto.user_id,
            banned=dto.banned,
        )
        return MutationResponseDTO(
            data=data,
            message="Participant banned successfully.",
        )
