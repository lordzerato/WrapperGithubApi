from fastapi import HTTPException
from httpx import AsyncClient
from app.models.types import OBJECT, Methods
from app.core.config import settings

GITHUB_TOKEN = settings.AUTH_TOKEN
GITHUB_API_URL = settings.GITHUB_API_URL
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

class GITHUB_CLIENT:
    @staticmethod
    async def client_request(
        endpoint: str,
        method: Methods,
        payload: OBJECT | None
    ):
        async with AsyncClient() as client:
            url = f"{GITHUB_API_URL}{endpoint}"
            response = await client.request(method, url, headers=headers, json=payload)
            status_code: int = response.status_code
            data_json = response.json()
            if "errors" in data_json:
                raise HTTPException(400, data_json["errors"])
            if status_code != 200:
                raise HTTPException(status_code, f"{data_json["message"]}")
            return data_json
