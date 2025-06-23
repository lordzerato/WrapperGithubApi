from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.services.github_client import get_user_details, get_user_repos, get_user_followers
from app.models.response_schema import ProfileResponse, RepositoriesResponse, FollowersResponse

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/{username}", response_model=ProfileResponse)
async def user_info(username: str):
    try:
        data = await get_user_details(username)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        status = getattr(e, "status", 500)
        raise HTTPException(status_code=status, detail=str(e))
    return data


@router.get("/{username}/repos", response_model=RepositoriesResponse)
async def user_repos(username: str):
    try:
        data = await get_user_repos(username)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        status = getattr(e, "status", 500)
        raise HTTPException(status_code=status, detail=str(e))
    return data

@router.get("/{username}/followers", response_model=FollowersResponse)
async def user_followers(username: str):
    try:
        data = await get_user_followers(username)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        status = getattr(e, "status", 500)
        raise HTTPException(status_code=status, detail=str(e))
    return data
