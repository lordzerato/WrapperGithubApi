from fastapi import APIRouter, HTTPException
from app.services.github_client import get_search_users, get_search_repos
from app.models.response_schema import SearchUsersResponse, SearchReposResponse

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/users", response_model=SearchUsersResponse)
async def search_users(query: str, page: int = 1, per_page: int = 5):
    if not query:
        raise HTTPException(status_code=400, detail="Missing query params")
    return await get_search_users(query, page, per_page)

@router.get("/repositories", response_model=SearchReposResponse)
async def search_repos(query: str, page: int = 1, limit: int = 5):
    if not query:
        raise HTTPException(status_code=400, detail="Missing query params")
    return await get_search_repos(query, page, limit)
