# application/usecases/create_meet_usecase.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from pydantic.dataclasses import dataclass

from domain.entity.meet_entity import Meet
from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository
from domain.repository_interface.user_repository_interface import IUserRepository
from domain.exceptions.base_exceptions import UnauthorizedRoleError, RoleHierarchyViolationError, InvalidParticipantError

@dataclass
class CreateMeetRequestInput:
    actor_id: int
    actor_role: Role
    title: str
    start_time: datetime
    expires_at: datetime
    guest_usernames: List[str]
    assign_to_username: Optional[str] = None

@dataclass
class CreateMeetResponseOutput:
    creator_id: int
    title: str
    start_time: datetime
    expires_at: datetime
    meet_hash: str
    id: int

class INotificationService(ABC):
    @abstractmethod
    def send_meet_invitation(self, user_id: int, meet_hash: str, title: str) -> None:
        pass

class CreateMeetUseCase:
    def __init__(self, meet_repository: IMeetRepository, user_repository: IUserRepository):
        self.meet_repository = meet_repository
        self.user_repository = user_repository

    def execute(self, request: CreateMeetRequestInput) -> CreateMeetResponseOutput:
        actor = self.user_repository.find_by_id(request.actor_id)
        if not actor:
            raise UnauthorizedRoleError("Authenticated user not found.")

        target_creator = actor
        if request.assign_to_username:
            target_user = self.user_repository.find_by_username(request.assign_to_username)
            if not target_user:
                raise InvalidParticipantError(f"Target creator '{request.assign_to_username}' not found.")
            if target_user.role not in [Role.Host, Role.Admin, Role.SuperAdmin]:
                raise InvalidParticipantError("Target creator must have a role of Host, Admin, or SuperAdmin.")
            target_creator = target_user

        
        is_assigning = (target_creator.id != actor.id)

        if request.actor_role == Role.Host:
            if is_assigning:
                raise RoleHierarchyViolationError("Hosts can only create meetings for themselves.")
                
        elif request.actor_role == Role.Admin:
            if is_assigning:
                if target_creator.role != Role.Host:
                    raise RoleHierarchyViolationError("Admins can only assign meetings to Hosts.")
                    
        elif request.actor_role == Role.SuperAdmin:
            pass
            
        elif request.actor_role == Role.User:
            raise UnauthorizedRoleError("Users do not have permission to create meetings.")
            
        else:
            raise UnauthorizedRoleError("Only SuperAdmins, Admins, or Hosts can create a meet.")

        participant_ids = []
        for username in request.guest_usernames:
            if username == target_creator.username:
                continue 
            guest = self.user_repository.find_by_username(username)
            if guest:
                participant_ids.append(guest.id)

        if len(participant_ids) == 0:
            raise InvalidParticipantError("At least one valid guest username must be provided.")

        new_meet = Meet(
            title=request.title,
            creator_id=target_creator.id,
            start_time=request.start_time,
            expires_at=request.expires_at,
            participants_ids=participant_ids,
        )

        saved_meet = self.meet_repository.save(new_meet)

        return CreateMeetResponseOutput(
            creator_id=saved_meet.creator_id,
            title=saved_meet.title,
            start_time=saved_meet.start_time,
            expires_at=saved_meet.expires_at,
            meet_hash=saved_meet.meet_hash,
            id=saved_meet.id,
        )