from pydantic.dataclasses import dataclass

from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository
from domain.repository_interface.participant_repository_interface import IParticipantRepository
from domain.exceptions.base_exceptions import ResourceNotFoundError, ForbiddenActionError, UserBannedError
from application.interfaces.livekit_service_interface import ILiveKitService


@dataclass
class GenerateLiveKitTokenRequestInput:
    meet_hash: str
    actor_id: int
    actor_role: Role


@dataclass
class GenerateLiveKitTokenResponseOutput:
    token: str
    room_name: str


class GenerateLiveKitTokenUseCase:
    def __init__(
        self,
        meet_repository: IMeetRepository,
        participant_repository: IParticipantRepository,
        livekit_service: ILiveKitService,
    ):
        self.meet_repository = meet_repository
        self.participant_repository = participant_repository
        self.livekit_service = livekit_service

    def execute(self, request: GenerateLiveKitTokenRequestInput) -> GenerateLiveKitTokenResponseOutput:
        meet = self.meet_repository.find_by_hash(request.meet_hash)
        if not meet:
            raise ResourceNotFoundError("Meeting not found.")

        is_creator = meet.creator_id == request.actor_id
        is_participant = request.actor_id in meet.participants_ids

        if request.actor_role == Role.SuperAdmin:
            pass
        elif request.actor_role == Role.Admin:
            pass
        elif request.actor_role == Role.Host:
            if not is_creator and not is_participant:
                raise ForbiddenActionError("You do not have access to this meeting.")
        elif request.actor_role == Role.User:
            if not is_participant:
                raise ForbiddenActionError("You do not have access to this meeting.")

        if not is_creator:
            banned = self.participant_repository.is_user_banned(meet.id, request.actor_id)
            if banned:
                raise UserBannedError()

        room_admin = is_creator
        identity = str(request.actor_id)
        room_name = request.meet_hash

        token = self.livekit_service.generate_join_token(
            identity=identity,
            room_name=room_name,
            room_admin=room_admin,
        )

        return GenerateLiveKitTokenResponseOutput(
            token=token,
            room_name=room_name,
        )
