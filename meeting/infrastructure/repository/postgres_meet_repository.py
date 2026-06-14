from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from domain.entity.meet_entity import Meet
from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository, MeetFilter
from infrastructure.orm.meet_model import MeetModel
from infrastructure.orm.participant_model import MeetParticipantModel
from infrastructure.orm.user_model import UserModel


class PostgresMeetRepository(IMeetRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, meet: Meet) -> Meet:
        if meet.id:
            db_meet = self.db_session.query(MeetModel).filter(MeetModel.id == meet.id).first()
            db_meet.title = meet.title
            db_meet.is_active = meet.is_active
            db_meet.update_at = meet.update_at
            db_meet.start_time = meet.start_time
            db_meet.expires_at = meet.expires_at
            db_meet.creator_id = meet.creator_id

            db_meet.participants.clear()
        else:
            db_meet = MeetModel(
                title=meet.title,
                meet_hash=meet.meet_hash,
                start_time=meet.start_time,
                expires_at=meet.expires_at,
                is_active=meet.is_active,
                creator_id=meet.creator_id,
                created_at=meet.created_at,
                update_at=meet.update_at,
            )

        for participant_id in meet.participants_ids:
            participant_record = MeetParticipantModel(user_id=participant_id)
            db_meet.participants.append(participant_record)

        self.db_session.add(db_meet)
        self.db_session.commit()
        self.db_session.refresh(db_meet)

        meet.id = db_meet.id
        return meet

    def find_by_hash(self, meet_hash: str) -> Meet | None:
        db_meet = self.db_session.query(MeetModel).filter(MeetModel.meet_hash == meet_hash).first()
        return self._map_to_domain(db_meet)

    def find_by_id(self, meet_id: int) -> Meet | None:
        db_meet = self.db_session.query(MeetModel).filter(MeetModel.id == meet_id).first()
        return self._map_to_domain(db_meet)

    def delete(self, meet_id: int) -> None:
        self.db_session.query(MeetModel).filter(MeetModel.id == meet_id).delete()
        self.db_session.commit()

    def find_paginated(self, filters: MeetFilter, page: int, size: int) -> Tuple[List[Meet], int]:
        query = self.db_session.query(MeetModel)

        query = self._apply_role_filter(query, filters)
        query = self._apply_extra_filters(query, filters)

        total = query.count()
        offset = (page - 1) * size
        db_meets = query.order_by(MeetModel.created_at.desc()).offset(offset).limit(size).all()

        meets = [self._map_to_domain(db_m) for db_m in db_meets if db_m]
        return meets, total

    def _apply_role_filter(self, query, filters: MeetFilter):
        if filters.actor_role in (Role.SuperAdmin, Role.Admin):
            return query

        if filters.actor_role == Role.Host:
            subquery = (
                self.db_session.query(MeetParticipantModel.meet_id)
                .filter(MeetParticipantModel.user_id == filters.actor_id)
                .subquery()
            )
            return query.filter(
                or_(
                    MeetModel.creator_id == filters.actor_id,
                    MeetModel.id.in_(subquery),
                )
            )

        if filters.actor_role == Role.User:
            subquery = (
                self.db_session.query(MeetParticipantModel.meet_id)
                .filter(MeetParticipantModel.user_id == filters.actor_id)
                .subquery()
            )
            return query.filter(MeetModel.id.in_(subquery))

        return query

    def _apply_extra_filters(self, query, filters: MeetFilter):
        if filters.creator_id is not None:
            query = query.filter(MeetModel.creator_id == filters.creator_id)

        if filters.participant_user_id is not None:
            subquery = (
                self.db_session.query(MeetParticipantModel.meet_id)
                .filter(MeetParticipantModel.user_id == filters.participant_user_id)
                .subquery()
            )
            query = query.filter(MeetModel.id.in_(subquery))

        if filters.start_date_from is not None:
            query = query.filter(MeetModel.start_time >= filters.start_date_from)

        if filters.start_date_to is not None:
            query = query.filter(MeetModel.start_time <= filters.start_date_to)

        if filters.guest_username is not None:
            query = query.filter(
                MeetModel.participants.any(
                    MeetParticipantModel.user.has(UserModel.username == filters.guest_username)
                )
            )

        if filters.title_query is not None:
            query = query.filter(MeetModel.title.ilike(f"%{filters.title_query}%"))

        return query

    def _map_to_domain(self, db_meet: MeetModel) -> Meet | None:
        if not db_meet:
            return None

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
