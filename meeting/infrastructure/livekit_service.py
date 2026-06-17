import os
from livekit.api import LiveKitAPI, AccessToken, VideoGrants
from application.interfaces.livekit_service_interface import ILiveKitService

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "devsecret")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "http://localhost:7880")


class LiveKitService(ILiveKitService):

    def generate_join_token(self, identity: str, room_name: str, room_admin: bool = False) -> str:
        token = AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)

        token = (
            token.with_identity(identity)
            .with_name(identity)
            .with_grants(
                VideoGrants(
                    room_join=True,
                    room=room_name,
                    room_admin=room_admin,
                )
            )
        )

        return token.to_jwt()

