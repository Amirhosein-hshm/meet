from pydantic.dataclasses import dataclass

from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository
from domain.repository_interface.participant_repository_interface import IParticipantRepository
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import (
    ResourceNotFoundError,
    ForbiddenActionError,
    InvalidParticipantError,
)
from application.interfaces.livekit_service_interface import ILiveKitService


@dataclass
class BanParticipantRequestInput:
    meet_hash: str
    actor_id: int
    actor_role: Role
    target_user_id: int


@dataclass
class BanParticipantResponseOutput:
    meet_hash: str
    user_id: int
    banned: bool


class BanParticipantUseCase:
    def __init__(
        self,
        meet_repository: IMeetRepository,
        participant_repository: IParticipantRepository,
        user_repository: IUserRepository,
        livekit_service: ILiveKitService,
    ):
        self.meet_repository = meet_repository
        self.participant_repository = participant_repository
        self.user_repository = user_repository
        self.livekit_service = livekit_service

    def execute(self, request: BanParticipantRequestInput) -> BanParticipantResponseOutput:
        meet = self.meet_repository.find_by_hash(request.meet_hash)
        if not meet:
            raise ResourceNotFoundError("Meeting not found.")

        if request.actor_role == Role.SuperAdmin:
            pass
        elif request.actor_role == Role.Admin:
            if meet.creator_id != request.actor_id:
                raise ForbiddenActionError("Admins can only ban in their own meetings.")
        elif request.actor_role == Role.Host:
            if meet.creator_id != request.actor_id:
                raise ForbiddenActionError("Only the meeting creator can ban participants.")
        else:
            raise ForbiddenActionError("You do not have permission to ban participants.")

        target_user = self.user_repository.find_by_id(request.target_user_id)
        if not target_user:
            raise ResourceNotFoundError("Target user not found.")

        participant = self.participant_repository.find_participant(meet.id, request.target_user_id)
        if not participant:
            raise InvalidParticipantError("User is not a participant of this meeting.")

        self.participant_repository.ban_user(meet.id, request.target_user_id)

        try:
            self.livekit_service.remove_participant(
                room_name=request.meet_hash,
                identity=str(request.target_user_id),
            )
        except Exception:
            pass

        return BanParticipantResponseOutput(
            meet_hash=request.meet_hash,
            user_id=request.target_user_id,
            banned=True,
        )
