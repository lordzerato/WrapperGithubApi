from fastapi import APIRouter
from app.services.github_client import get_search_users, get_search_repos
from app.models.response_schema import SearchUsersResponse, SearchReposResponse

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/users", response_model=SearchUsersResponse)
async def search_users(q: str, p: int = 1, limit: int = 5):
    data = await get_search_users(q, p, limit)
    users = SearchUsersResponse.model_validate(data)
    return users

@router.get("/repositories", response_model=SearchReposResponse)
async def search_repos(q: str, p: int = 1, limit: int = 5):
    data = await get_search_repos(q, p, limit)
    repos = SearchReposResponse.model_validate(data)
    return repos
