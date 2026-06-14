from sqlalchemy.orm import Session
from domain.repository_interface.refresh_token_repository_interface import IRefreshTokenRepository
from infrastructure.orm.refresh_token_model import RefreshTokenModel

class PostgresRefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, user_id: int, token: str) -> None:
        new_token = RefreshTokenModel(user_id=user_id, token=token)
        self.db_session.add(new_token)
        self.db_session.commit()

    def is_valid(self, user_id: int, token: str) -> bool:
        db_token = self.db_session.query(RefreshTokenModel).filter(
            RefreshTokenModel.user_id == user_id,
            RefreshTokenModel.token == token
        ).first()
        return db_token is not None

    def revoke(self, user_id: int, token: str) -> None:
        self.db_session.query(RefreshTokenModel).filter(
            RefreshTokenModel.user_id == user_id,
            RefreshTokenModel.token == token
        ).delete(synchronize_session=False)
        self.db_session.commit()