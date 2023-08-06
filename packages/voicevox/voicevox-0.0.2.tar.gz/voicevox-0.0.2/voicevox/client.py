# voicevox - Client

from typing import Any, Optional

from httpx import AsyncClient

from .errors import NotfoundError, HttpException
from .types import AudioQueryType
from .audio_query import AudioQuery


class Client:
    session: AsyncClient
    base_url: str

    def __init__(self, base_url: str = "http://localhost:50021"):
        self.base_url = base_url
        self.session = AsyncClient(base_url=base_url)

    async def close(self) -> None:
        await self.session.aclose()

    async def request(self, method: str, path: str, **kwargs) -> dict:
        response = await self.session.request(method, path, **kwargs)
        if response.status_code == 200:
            if response.headers["content-type"] == "application/json":
                return response.json()
            else:
                return response.content
        elif response.status_code == 404:
            raise NotfoundError(response.json()["detail"])
        else:
            raise HttpException(response.json())

    async def synthesis(
        self, speaker: int, audio_query: AudioQueryType, *,
        enable_interrogative_upspeak: bool = True,
        core_version: Optional[str] = None
    ) -> bytes:
        parameters = {
            "speaker": speaker,
            "enable_interrogative_upspeak": enable_interrogative_upspeak
        }
        if core_version is not None:
            parameters["core_version"] = core_version
        return await self.request(
            "POST", "/synthesis", params=parameters,
            json=audio_query
        )

    async def create_audio_query(
        self, text: int, speaker: int, *, core_version: Optional[str] = None
    ) -> AudioQuery:
        params = {
            "text": text,
            "speaker": speaker
        }
        if core_version is not None:
            params["core_version"] = core_version
        audio_query = await self.request(
            "POST", "/audio_query", params=params
        )
        return AudioQuery(self, audio_query, speaker)

    async def create_audio_query_from_preset(
        self, text: str, preset_id: int, *, core_version: Optional[str] = None
    ) -> AudioQuery:
        params = {
            "text": text,
            "preset_id": preset_id
        }
        if core_version is not None:
            params["core_version"] = core_version
        audio_query = await self.request(
            "POST", "/audio_query_from_preset", params=params
        )
        return AudioQuery(self, audio_query, preset_id)