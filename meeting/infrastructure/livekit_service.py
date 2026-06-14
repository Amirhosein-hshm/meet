import os
from livekit import api
from livekit.protocol import models as livekit_models

from application.interfaces.livekit_service_interface import ILiveKitService


LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "devsecret")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")


class LiveKitService(ILiveKitService):
    def __init__(self) -> None:
        token_service = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        self._token_service = token_service
        self._room_service = api.RoomServiceClient(
            LIVEKIT_URL,
            LIVEKIT_API_KEY,
            LIVEKIT_API_SECRET,
        )

    def generate_join_token(self, identity: str, room_name: str, room_admin: bool = False) -> str:
        token = self._token_service.with_identity(identity).with_name(identity).with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
                room_admin=room_admin,
            )
        )
        return token.to_jwt()

    def remove_participant(self, room_name: str, identity: str) -> None:
        self._room_service.remove_participant(room_name, identity)
