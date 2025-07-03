import httpx
from fastapi import HTTPException
from cachetools import TTLCache
from typing import Any
from app.core.config import settings
from app.models.response_schema import (
    RepositoriesResponse,
    RepositoryDetailsResponse,
    RepositoryActivityResponse,
    RepositoryContributorsResponse,
    RepositoryBranchesResponse,
    RepositoryIssuesResponse,
    RepositoryPullsResponse,
    RepositorySubscribersResponse,
    RepositoryStargazersResponse,
    RepositoryLanguagesResponse,
    ProfileResponse,
    UsersRepositoriesResponse,
    FollowersResponse,
    SearchUsersResponse,
    SearchReposResponse,
    GraphQLSearchUsersResponse
)
from app.models.graphql import Variables

# max 500 items & expired after 5 minutes
repo_cache: TTLCache[
    str,
    RepositoriesResponse
    | RepositoryDetailsResponse
    | UsersRepositoriesResponse
    | RepositoryActivityResponse
    | RepositoryContributorsResponse
    | RepositoryBranchesResponse
    | RepositoryIssuesResponse
    | RepositoryPullsResponse
    | RepositorySubscribersResponse
    | RepositoryStargazersResponse
    | RepositoryLanguagesResponse
    | ProfileResponse
    | FollowersResponse
    | SearchUsersResponse
    | SearchReposResponse
    | GraphQLSearchUsersResponse
] = TTLCache(maxsize=500, ttl=300)
other_cache: TTLCache[str, dict[str, Any]] = TTLCache(maxsize=500, ttl=300)
GITHUB_TOKEN = settings.AUTH_TOKEN
GITHUB_API_URL = settings.GITHUB_API_URL
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

async def get_public_repositories(query: str) -> RepositoriesResponse:
    if cache := repo_cache.get("repositories{query}"):
        return RepositoriesResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}repositories{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"Repositories {data_json["message"]}")
        data = RepositoriesResponse.model_validate(data_json)
        repo_cache["repositories{query}"] = data
        return data

async def get_repo_details(username: str, repo: str) -> RepositoryDetailsResponse:
    if cache := repo_cache.get("repos/{username}/{repo}"):
        return RepositoryDetailsResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}repos/{username}/{repo}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User / Repository {data_json["message"]}")
        data = RepositoryDetailsResponse.model_validate(data_json)
        repo_cache["repos/{username}/{repo}"] = data
        return data

async def get_repo_activity(username: str, repo: str, query: str) -> RepositoryActivityResponse:
    if cache := repo_cache.get("repos/{username}/{repo}/activity{query}"):
        return RepositoryActivityResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}repos/{username}/{repo}/activity{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User / Repository {data_json["message"]}")
        data = RepositoryActivityResponse.model_validate(data_json)
        repo_cache["repos/{username}/{repo}/activity{query}"] = data
        return data

async def get_repo_contributors(username: str, repo: str, query: str) -> RepositoryContributorsResponse:
    if cache := repo_cache.get("repos/{username}/{repo}/contributors{query}"):
        return RepositoryContributorsResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}repos/{username}/{repo}/contributors{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User / Repository {data_json["message"]}")
        data = RepositoryContributorsResponse.model_validate(data_json)
        repo_cache["repos/{username}/{repo}/contributors{query}"] = data
        return data

async def get_repo_branches(username: str, repo: str, query: str) -> RepositoryBranchesResponse:
    if cache := repo_cache.get("repos/{username}/{repo}/branches{query}"):
        return RepositoryBranchesResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}repos/{username}/{repo}/branches{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User / Repository {data_json["message"]}")
        data = RepositoryBranchesResponse.model_validate(data_json)
        repo_cache["repos/{username}/{repo}/branches{query}"] = data
        return data

async def get_repo_issues(username: str, repo: str, query: str) -> RepositoryIssuesResponse:
    if cache := repo_cache.get("repos/{username}/{repo}/issues{query}"):
        return RepositoryIssuesResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}repos/{username}/{repo}/issues{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User / Repository {data_json["message"]}")
        data = RepositoryIssuesResponse.model_validate(data_json)
        repo_cache["repos/{username}/{repo}/issues{query}"] = data
        return data

async def get_repo_pulls(username: str, repo: str, query: str) -> RepositoryPullsResponse:
    if cache := repo_cache.get("repos/{username}/{repo}/pulls{query}"):
        return RepositoryPullsResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}repos/{username}/{repo}/pulls{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User / Repository {data_json["message"]}")
        data = RepositoryPullsResponse.model_validate(data_json)
        repo_cache["repos/{username}/{repo}/pulls{query}"] = data
        return data

async def get_repo_subscribers(username: str, repo: str, query: str) -> RepositorySubscribersResponse:
    if cache := repo_cache.get("repos/{username}/{repo}/subscribers{query}"):
        return RepositorySubscribersResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}repos/{username}/{repo}/subscribers{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User / Repository {data_json["message"]}")
        data = RepositorySubscribersResponse.model_validate(data_json)
        repo_cache["repos/{username}/{repo}/subscribers{query}"] = data
        return data

async def get_repo_stargazers(username: str, repo: str, query: str) -> RepositoryStargazersResponse:
    if cache := repo_cache.get("repos/{username}/{repo}/stargazers{query}"):
        return RepositoryStargazersResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}repos/{username}/{repo}/stargazers{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User / Repository {data_json["message"]}")
        data = RepositoryStargazersResponse.model_validate(data_json)
        repo_cache["repos/{username}/{repo}/stargazers{query}"] = data
        return data

async def get_repo_languages(username: str, repo: str) -> RepositoryLanguagesResponse:
    if cache := repo_cache.get("repos/{username}/{repo}/languages"):
        return RepositoryLanguagesResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}repos/{username}/{repo}/languages"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User / Repository {data_json["message"]}")
        data = RepositoryLanguagesResponse.model_validate(data_json)
        repo_cache["repos/{username}/{repo}/languages"] = data
        return data

async def get_user_details(username: str) -> ProfileResponse:
    if cache := repo_cache.get("{username}/details"):
        return ProfileResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}users/{username}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User {data_json["message"]}")
        data = ProfileResponse.model_validate(data_json)
        repo_cache["{username}/details"] = data
        return data

async def get_user_repos(username: str, query: str) -> UsersRepositoriesResponse:
    if cache := repo_cache.get("{username}/repos{query}"):
        return UsersRepositoriesResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}users/{username}/repos{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User {data_json["message"]}")
        data = UsersRepositoriesResponse.model_validate(data_json)
        repo_cache["{username}/repos{query}"] = data
        return data

async def get_user_followers(username: str, query: str) -> FollowersResponse:
    if cache := repo_cache.get("{username}/followers{query}"):
        return FollowersResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}users/{username}/followers{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(response.status_code, f"User {data_json["message"]}")
        data = FollowersResponse.model_validate(data_json)
        repo_cache["{username}/followers{query}"] = data
        return data

async def get_search_users(query: str) -> SearchUsersResponse:
    if cache := repo_cache.get("search/users{query}"):
        return SearchUsersResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}search/users{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(
                status_code = response.status_code,
                detail = data_json.get("errors")
            )
        data = SearchUsersResponse.model_validate(data_json)
        repo_cache["search/users{query}"] = data
        return data

async def get_search_repos(query: str) -> SearchReposResponse:
    if cache := repo_cache.get("search/repositories{query}"):
        return SearchReposResponse.model_validate(cache)
    url = f"{GITHUB_API_URL}search/repositories{query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data_json = response.json()
        if response.status_code != 200:
            raise HTTPException(
                status_code = response.status_code,
                detail = data_json.get("errors")
            )
        data = SearchReposResponse.model_validate(data_json)
        repo_cache["search/repositories{query}"] = data
        return data

async def graphql_request(query: str, variables: Variables) -> dict[str, Any]:
    if cache := other_cache.get("graphql/{query}&{variables}"):
        return cache
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
        other_cache["graphql/{query}&{variables}"] = data
        return data

async def graphql_search_users(
    username: str, page: str | None, per_page: int
) -> GraphQLSearchUsersResponse:
    if cache := repo_cache.get(
        "graphql-search-users/{username}&p={page}&limit={per_page}"
    ):
        return GraphQLSearchUsersResponse.model_validate(cache)
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
        repo_cache["graphql-search-users/{username}&p={page}&limit={per_page}"] = data
        return data
