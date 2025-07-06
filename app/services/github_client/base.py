from httpx import AsyncClient
from typing import Literal
from app.models.types import JSON
from app.core.config import settings

GITHUB_TOKEN = settings.AUTH_TOKEN
GITHUB_API_URL = settings.GITHUB_API_URL
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

class GITHUB_CLIENT:
    @staticmethod
    async def client_request(
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE"] = "GET",
        payload: JSON | None = None
    ):
        async with AsyncClient() as client:
            url = f"{GITHUB_API_URL}{endpoint}"
            response = await client.request(method, url, headers=headers, json=payload)
            data: JSON = {
                "status_code": response.status_code,
                "data": response.json()
            }
            return data
    