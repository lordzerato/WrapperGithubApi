from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.services.github_client import get_search_users, get_search_repos
from app.models.response_schema import SearchUsersResponse, SearchReposResponse

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/users", response_model=SearchUsersResponse)
async def search_users(q: str, p: int = 1, limit: int = 5):
    try:
        data = await get_search_users(q, p, limit)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return data

@router.get("/repositories", response_model=SearchReposResponse)
async def search_repos(q: str, p: int = 1, limit: int = 5):
    try:
        data = await get_search_repos(q, p, limit)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return data
