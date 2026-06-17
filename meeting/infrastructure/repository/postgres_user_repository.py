from typing import List, Tuple
from sqlalchemy.orm import Session
from domain.entity.user_entity import User
from domain.repository_interface.user_repository_interface import IUserRepository
from infrastructure.orm.refresh_token_model import RefreshTokenModel
from infrastructure.orm.user_model import UserModel

class PostgresUserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, user: User) -> User:
        if user.id:
            db_user = self.db_session.query(UserModel).filter(UserModel.id == user.id).first()
            if db_user:
                db_user.first_name = user.first_name
                db_user.last_name = user.last_name
                db_user.username = user.username
                db_user.email = user.email
                db_user.password_hash = user.password_hash
                db_user.role = user.role
                db_user.is_active = user.is_active
                db_user.update_at = user.update_at
        else:
            db_user = UserModel(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at,
                update_at=user.update_at,
            )
            self.db_session.add(db_user)

        self.db_session.commit()
        self.db_session.refresh(db_user)

        user.id = db_user.id
        return user

    def find_by_username(self, username: str) -> User | None:
        db_user = self.db_session.query(UserModel).filter(UserModel.username == username).first()
        if not db_user:
            return None
        return User(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password_hash,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            update_at=db_user.update_at
        )


    def find_by_email(self, email: str) -> User | None:
        db_user = self.db_session.query(UserModel).filter(UserModel.email == email).first()
        if not db_user:
            return None
        return User(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password_hash,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            update_at=db_user.update_at
        )
    
    def find_by_id(self, user_id: int) -> User | None:
        db_user = self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None
        return User(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password_hash,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            update_at=db_user.update_at
        )

    def find_all_paginated(self, page: int, size: int) -> Tuple[List[User], int]:
        query = self.db_session.query(UserModel)
        total = query.count()
        offset = (page - 1) * size
        db_users = query.order_by(UserModel.created_at.desc()).offset(offset).limit(size).all()
        users = [
            User(
                id=u.id,
                first_name=u.first_name,
                last_name=u.last_name,
                username=u.username,
                email=u.email,
                password_hash=u.password_hash,
                role=u.role,
                is_active=u.is_active,
                created_at=u.created_at,
                update_at=u.update_at,
            )
            for u in db_users
        ]
        return users, total

    def delete(self, user_id: int) -> None:
        self.db_session.query(UserModel).filter(UserModel.id == user_id).delete()
        self.db_session.commit()
    