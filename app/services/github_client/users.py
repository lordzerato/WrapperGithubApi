from fastapi import HTTPException
from cachetools import TTLCache
from .base import GITHUB_CLIENT
from app.models.types import JSON
from app.models.response_schema import (
    UsersDetailsResponse,
    UsersRepositoriesResponse,
    UsersFollowersResponse,
    UsersStarredResponse,
    UsersPublicEventsResponse
)

repo_cache: TTLCache[str, JSON] = TTLCache(maxsize=500, ttl=300)
client = GITHUB_CLIENT.client_request

async def get_user_details(username: str) -> UsersDetailsResponse:
    endpoint: str = f"users/{username}"
    if cache := repo_cache.get(endpoint):
        return UsersDetailsResponse.model_validate(cache)
    response = await client(endpoint)
    status_code: int = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User {data_json["message"]}")
    data = UsersDetailsResponse.model_validate(data_json)
    return data


async def get_user_repos(username: str, query: str) -> UsersRepositoriesResponse:
    endpoint: str = f"users/{username}/repos{query}"
    if cache := repo_cache.get(endpoint):
        return UsersRepositoriesResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User {data_json["message"]}")
    data = UsersRepositoriesResponse.model_validate(data_json)
    return data

async def get_user_followers(username: str, query: str) -> UsersFollowersResponse:
    endpoint: str = f"users/{username}/followers{query}"
    if cache := repo_cache.get(endpoint):
        return UsersFollowersResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User {data_json["message"]}")
    data = UsersFollowersResponse.model_validate(data_json)
    return data

async def get_user_starred(username: str, query: str) -> UsersStarredResponse:
    endpoint: str = f"users/{username}/starred{query}"
    if cache := repo_cache.get(endpoint):
        return UsersStarredResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User {data_json["message"]}")
    data = UsersStarredResponse.model_validate(data_json)
    return data

async def get_user_public_event(username: str, query: str) -> UsersPublicEventsResponse:
    endpoint: str = f"users/{username}/events/public{query}"
    if cache := repo_cache.get(endpoint):
        return UsersPublicEventsResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User {data_json["message"]}")
    data = UsersPublicEventsResponse.model_validate(data_json)
    return data
