from fastapi import HTTPException
from cachetools import TTLCache
from .base import GITHUB_CLIENT
from app.models.types import JSON, GraphQLVariables
from app.models.response_schema import GraphQLSearchUsersResponse, GraphQLResponse
from app.utils.utils import get_hash_value

repo_cache: TTLCache[str, JSON] = TTLCache(maxsize=500, ttl=300)
client = GITHUB_CLIENT.client_request

async def graphql_request(query: str, variables: GraphQLVariables) -> GraphQLResponse:
    payload: dict[str, str | GraphQLVariables] = {
        "query": query,
        "variables": variables if variables else {}
    }
    hash = get_hash_value(payload)
    key = f"graphql/{hash}"
    if cache := repo_cache.get(key):
        return GraphQLResponse.model_validate(cache)
    endpoint = "graphql"
    response = await client(endpoint, "POST", payload)
    data_json = response.get("data", {"errors": "Unknown Error"})
    repo_cache[key] = data_json
    if "errors" in data_json:
        raise HTTPException(status_code=400, detail=data_json["errors"])
    data = GraphQLResponse.model_validate(data_json)
    return data

async def graphql_search_users(
    username: str, page: str | None, per_page: int
) -> GraphQLSearchUsersResponse:
    key = f"graphql-search-users?q={username}&page={page}&per_page={per_page}"
    if cache := repo_cache.get(key):
        return GraphQLSearchUsersResponse.model_validate(cache)
    endpoint = "graphql"
    query = "query SearchUsers($login: String!, $first: Int = 5, $after: String = null) { search(type: USER, query: $login, first: $first, after: $after) { userCount pageInfo { hasNextPage endCursor } edges { node { ... on User { login name avatarUrl bio company location url}}}}}"
    variables: GraphQLVariables = {"login": username, "after": page, "first": per_page}
    payload: dict[str, str | GraphQLVariables] = {
        "query": query,
        "variables": variables
    }
    response = await client(endpoint, "POST", payload)
    data_json = response.get("data", {"errors": "Unknown Error"})
    repo_cache[key] = data_json
    if "errors" in data_json:
        raise HTTPException(status_code=400, detail=data_json["errors"])
    data = GraphQLSearchUsersResponse.model_validate(data_json)
    return data