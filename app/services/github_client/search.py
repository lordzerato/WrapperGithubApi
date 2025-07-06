from fastapi import HTTPException
from cachetools import TTLCache
from .base import GITHUB_CLIENT
from app.models.types import JSON
from app.models.response_schema import SearchUsersResponse, SearchReposResponse

repo_cache: TTLCache[str, JSON] = TTLCache(maxsize=500, ttl=300)
client = GITHUB_CLIENT.client_request

async def get_search_users(query: str) -> SearchUsersResponse:
    endpoint: str = f"search/users{query}"
    if cache := repo_cache.get(endpoint):
        return SearchUsersResponse.model_validate(cache)
    response = await client(endpoint)
    status_code: int = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(
            status_code = status_code,
            detail = data_json.get("errors")
        )
    data = SearchUsersResponse.model_validate(data_json)
    return data

async def get_search_repos(query: str) -> SearchReposResponse:
    endpoint: str = f"search/repositories{query}"
    if cache := repo_cache.get(endpoint):
        return SearchReposResponse.model_validate(cache)
    response = await client(endpoint)
    status_code: int = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(
            status_code = status_code,
            detail = data_json.get("errors")
        )
    data = SearchReposResponse.model_validate(data_json)
    return data
