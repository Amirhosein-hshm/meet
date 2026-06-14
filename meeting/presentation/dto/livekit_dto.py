from pydantic import BaseModel


class LiveKitTokenData(BaseModel):
    token: str
    room_name: str


class BanParticipantResponseData(BaseModel):
    meet_hash: str
    user_id: int
    banned: bool
