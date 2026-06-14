from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from domain.entity.user_entity import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user_stub(token: str = Depends(oauth2_scheme)) -> User:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")