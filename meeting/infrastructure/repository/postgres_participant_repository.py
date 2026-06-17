from typing import List, Optional
from sqlalchemy.orm import Session

from domain.entity.meet_entity import Meet
from domain.repository_interface.participant_repository_interface import IParticipantRepository, ParticipantData
from infrastructure.orm.meet_model import MeetModel
from infrastructure.orm.participant_model import MeetParticipantModel


class PostgresParticipantRepository(IParticipantRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_invitations(self, user_id: int) -> List[Meet]:
        meet_models = (
            self.db_session.query(MeetModel)
            .join(MeetParticipantModel)
            .filter(MeetParticipantModel.user_id == user_id)
            .all()
        )
        return [self._map_meet_to_domain(m) for m in meet_models]

    def find_participant(self, meet_id: int, user_id: int) -> Optional[ParticipantData]:
        record = (
            self.db_session.query(MeetParticipantModel)
            .filter(
                MeetParticipantModel.meet_id == meet_id,
                MeetParticipantModel.user_id == user_id,
            )
            .first()
        )
        if not record:
            return None
        return ParticipantData(
            meet_id=record.meet_id,
            user_id=record.user_id,
            joined_at=record.joined_at,
        )

    def _map_meet_to_domain(self, db_meet: MeetModel) -> Meet:
        participant_ids = [p.user_id for p in db_meet.participants]
        return Meet(
            id=db_meet.id,
            title=db_meet.title,
            creator_id=db_meet.creator_id,
            start_time=db_meet.start_time,
            expires_at=db_meet.expires_at,
            meet_hash=db_meet.meet_hash,
            participants_ids=participant_ids,
            is_active=db_meet.is_active,
            created_at=db_meet.created_at,
            update_at=db_meet.update_at,
        )
