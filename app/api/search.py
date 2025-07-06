from fastapi import APIRouter, HTTPException
from typing import Literal
from app.services.github_client.search import get_search_users, get_search_repos
from app.models.response_schema import SearchUsersResponse, SearchReposResponse
from app.utils.utils import join_query_params

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/users", response_model=SearchUsersResponse)
async def search_users(
    q: str,
    sort: Literal["stars", "forks", "help-wanted-issues", "updated"] | None = None,
    order: Literal["desc", "asc"] = "desc",
    page: int = 1,
    per_page: int = 30
):
    if not q:
        raise HTTPException(status_code=400, detail="Missing query params")
    query_params: str = join_query_params({
        "sort": sort,
        "order": order,
        "page": page,
        "per_page": per_page
    })
    return await get_search_users(query_params)

@router.get("/repositories", response_model=SearchReposResponse)
async def search_repos(
    q: str,
    sort: Literal["stars", "forks", "help-wanted-issues", "updated"] | None = None,
    order: Literal["desc", "asc"] = "desc",
    page: int = 1,
    per_page: int = 30
):
    if not q:
        raise HTTPException(status_code=400, detail="Missing query params")
    query_params: str = join_query_params({
        "q": q,
        "sort": sort,
        "order": order,
        "page": page,
        "per_page": per_page
    })
    return await get_search_repos(query_params)
