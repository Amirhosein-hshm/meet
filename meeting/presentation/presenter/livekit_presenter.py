from application.usecases.generate_livekit_token_usecase import GenerateLiveKitTokenResponseOutput
from presentation.dto.livekit_dto import LiveKitTokenData
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
            message="توکن LiveKit با موفقیت تولید شد.",
        )
