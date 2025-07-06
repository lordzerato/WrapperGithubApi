from fastapi import HTTPException
from cachetools import TTLCache
from .base import GITHUB_CLIENT
from app.models.types import JSON
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
    RepositoryTopicsResponse,
    RepositoryReadmeResponse
)

repo_cache: TTLCache[str, JSON] = TTLCache(maxsize=500, ttl=300)
client = GITHUB_CLIENT.client_request

async def get_public_repositories(query: str) -> RepositoriesResponse:
    endpoint: str = f"repositories{query}"
    if cache := repo_cache.get(endpoint):
        return RepositoriesResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"Repositories {data_json["message"]}")
    data = RepositoriesResponse.model_validate(data_json)
    return data

async def get_repo_details(username: str, repo: str) -> RepositoryDetailsResponse:
    endpoint: str = f"repos/{username}/{repo}"
    if cache := repo_cache.get(endpoint):
        return RepositoryDetailsResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositoryDetailsResponse.model_validate(data_json)
    return data

async def get_repo_activity(username: str, repo: str, query: str) -> RepositoryActivityResponse:
    endpoint: str = f"repos/{username}/{repo}/activity{query}"
    if cache := repo_cache.get(endpoint):
        return RepositoryActivityResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositoryActivityResponse.model_validate(data_json)
    return data

async def get_repo_contributors(username: str, repo: str, query: str) -> RepositoryContributorsResponse:
    endpoint: str = f"repos/{username}/{repo}/contributors{query}"
    if cache := repo_cache.get(endpoint):
        return RepositoryContributorsResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositoryContributorsResponse.model_validate(data_json)
    return data

async def get_repo_branches(username: str, repo: str, query: str) -> RepositoryBranchesResponse:
    endpoint: str = f"repos/{username}/{repo}/branches{query}"
    if cache := repo_cache.get(endpoint):
        return RepositoryBranchesResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositoryBranchesResponse.model_validate(data_json)
    return data

async def get_repo_issues(username: str, repo: str, query: str) -> RepositoryIssuesResponse:
    endpoint: str = f"repos/{username}/{repo}/issues{query}"
    if cache := repo_cache.get(endpoint):
        return RepositoryIssuesResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositoryIssuesResponse.model_validate(data_json)
    return data

async def get_repo_pulls(username: str, repo: str, query: str) -> RepositoryPullsResponse:
    endpoint: str = f"repos/{username}/{repo}/pulls{query}"
    if cache := repo_cache.get(endpoint):
        return RepositoryPullsResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositoryPullsResponse.model_validate(data_json)
    return data

async def get_repo_subscribers(username: str, repo: str, query: str) -> RepositorySubscribersResponse:
    endpoint: str = f"repos/{username}/{repo}/subscribers{query}"
    if cache := repo_cache.get(endpoint):
        return RepositorySubscribersResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositorySubscribersResponse.model_validate(data_json)
    return data

async def get_repo_stargazers(username: str, repo: str, query: str) -> RepositoryStargazersResponse:
    endpoint: str = f"repos/{username}/{repo}/stargazers{query}"
    if cache := repo_cache.get(endpoint):
        return RepositoryStargazersResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositoryStargazersResponse.model_validate(data_json)
    return data

async def get_repo_languages(username: str, repo: str) -> RepositoryLanguagesResponse:
    endpoint: str = f"repos/{username}/{repo}/languages"
    if cache := repo_cache.get(endpoint):
        return RepositoryLanguagesResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositoryLanguagesResponse.model_validate(data_json)
    return data

async def get_repo_topics(username: str, repo: str, query: str) -> RepositoryTopicsResponse:
    endpoint: str = f"repos/{username}/{repo}/topics{query}"
    if cache := repo_cache.get(endpoint):
        return RepositoryTopicsResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositoryTopicsResponse.model_validate(data_json)
    return data

async def get_repo_readme(username: str, repo: str, query: str) -> RepositoryReadmeResponse:
    endpoint: str = f"repos/{username}/{repo}/readme{query}"
    if cache := repo_cache.get(endpoint):
        return RepositoryReadmeResponse.model_validate(cache)
    response = await client(endpoint)
    status_code = response.get("status_code", 500)
    data_json = response.get("data", {"message": "Unknown Error"})
    repo_cache[endpoint] = data_json
    if status_code != 200:
        raise HTTPException(status_code, f"User / Repository {data_json["message"]}")
    data = RepositoryReadmeResponse.model_validate(data_json)
    return data
