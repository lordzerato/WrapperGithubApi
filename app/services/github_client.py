import httpx
from fastapi import HTTPException
from cachetools import TTLCache
from typing import Any
from app.core.config import settings
from app.models.response_schema import (
    RepositoryDetailsResponse,
    ProfileResponse,
    RepositoriesResponse,
    FollowersResponse,
    SearchUsersResponse,
    SearchReposResponse,
    GraphQLSearchUsersResponse
)
from app.models.graphql import Variables

# max 500 items & expired after 5 minutes
repo_cache: TTLCache[
    str,
    RepositoryDetailsResponse
    | ProfileResponse
    | RepositoriesResponse
    | FollowersResponse
    | SearchUsersResponse
    | SearchReposResponse
    | GraphQLSearchUsersResponse
] = TTLCache(maxsize=500, ttl=300)
other_cache: TTLCache[str, dict[str, Any]] = TTLCache(maxsize=500, ttl=300)
GITHUB_TOKEN = f"Bearer {settings.AUTH_TOKEN}"
GITHUB_API_URL = settings.GITHUB_API_URL

async def get_repo_details(username: str, repo: str) -> RepositoryDetailsResponse:
    if cache := repo_cache.get(f"repos/{username}/{repo}"):
        return RepositoryDetailsResponse.model_validate(cache)
    headers = {"Authorization": GITHUB_TOKEN}
    url = f"{GITHUB_API_URL}repos/{username}/{repo}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User / Repository {data_json["message"]}")
        data = RepositoryDetailsResponse.model_validate(data_json)
        repo_cache[f"repos/{username}/{repo}"] = data
        return data

async def get_user_details(username: str) -> ProfileResponse:
    if cache := repo_cache.get(f"{username}/details"):
        return ProfileResponse.model_validate(cache)
    headers = {"Authorization": GITHUB_TOKEN}
    url = f"{GITHUB_API_URL}users/{username}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User {data_json["message"]}")
        data = ProfileResponse.model_validate(data_json)
        repo_cache[f"{username}/details"] = data
        return data

async def get_user_repos(username: str) -> RepositoriesResponse:
    if cache := repo_cache.get(f"{username}/repos"):
        return RepositoriesResponse.model_validate(cache)
    headers = {"Authorization": GITHUB_TOKEN}
    url = f"{GITHUB_API_URL}users/{username}/repos"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User {data_json["message"]}")
        data = RepositoriesResponse.model_validate(data_json)
        repo_cache[f"{username}/repos"] = data
        return data

async def get_user_followers(username: str) -> FollowersResponse:
    if cache := repo_cache.get(f"{username}/followers"):
        return FollowersResponse.model_validate(cache)
    headers = {"Authorization": GITHUB_TOKEN}
    url = f"{GITHUB_API_URL}users/{username}/followers"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User {data_json["message"]}")
        data = FollowersResponse.model_validate(data_json)
        repo_cache[f"{username}/followers"] = data
        return data

async def get_search_users(q: str, p: int = 1, limit: int = 5) -> SearchUsersResponse:
    if cache := repo_cache.get(f"search-user/{q}&page={p}&per_page={limit}"):
        return SearchUsersResponse.model_validate(cache)
    headers = {"Authorization": GITHUB_TOKEN}
    url = f"{GITHUB_API_URL}search/users?q={q}+in%3Alogin+type%3Auser&page={p}&per_page={limit}&type=users"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(
                status_code = response.status_code,
                detail = data_json.get("errors")
            )
        data = SearchUsersResponse.model_validate(data_json)
        repo_cache[f"search-user/{q}&page={p}&per_page={limit}"] = data
        return data

async def get_search_repos(q: str, p: int = 1, limit: int = 5) -> SearchReposResponse:
    if cache := repo_cache.get(f"search-repos/{q}&page={p}&per_page={limit}"):
        return SearchReposResponse.model_validate(cache)
    headers = {"Authorization": GITHUB_TOKEN}
    url = f"{GITHUB_API_URL}search/repositories?q={q}&page={p}&per_page={limit}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(
                status_code = response.status_code,
                detail = data_json.get("errors")
            )
        data = SearchReposResponse.model_validate(data_json)
        repo_cache[f"search-repos/{q}&page={p}&per_page={limit}"] = data
        return data

async def graphql_request(query: str, variables: Variables) -> dict[str, Any]:
    if cache := other_cache.get(f"graphql/{query}&{variables}"):
        return cache
    headers = {"Authorization": GITHUB_TOKEN}
    url = f"{GITHUB_API_URL}graphql"
    payload: dict[str, str | Variables] = {
        "query": query,
        "variables": variables if variables else {}
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        data = response.json()
        if "errors" in data:
            raise HTTPException(status_code = 400, detail = data.get("errors"))
        other_cache[f"graphql/{query}&{variables}"] = data
        return data

async def graphql_search_users(
    username: str, page: str | None, per_page: int
) -> GraphQLSearchUsersResponse:
    if cache := repo_cache.get(
        f"graphql-search-users/{username}&p={page}&limit={per_page}"
    ):
        return GraphQLSearchUsersResponse.model_validate(cache)
    headers = {"Authorization": GITHUB_TOKEN}
    url = f"{GITHUB_API_URL}graphql"
    query = "query SearchUsers($login: String!, $first: Int = 5, $after: String = null) { search(type: USER, query: $login, first: $first, after: $after) { userCount pageInfo { hasNextPage endCursor } edges { node { ... on User { login name avatarUrl bio company location url}}}}}"
    variables: Variables = {"login": username, "after": page, "first": per_page}
    payload: dict[str, str | Variables] = {"query": query, "variables": variables}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        data_json = response.json()
        if "errors" in data_json:
            raise HTTPException(status_code=400, detail=data_json)
        data = GraphQLSearchUsersResponse.model_validate(data_json)
        repo_cache[f"graphql-search-users/{username}&p={page}&limit={per_page}"] = data
        return data
