from pydantic import BaseModel


class LiveKitTokenData(BaseModel):
    token: str
    room_name: str
