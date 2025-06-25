from fastapi import APIRouter, HTTPException
from app.services.github_client import (
    get_user_details,
    get_user_repos,
    get_user_followers
)
from app.models.response_schema import (
    ProfileResponse,
    RepositoriesResponse,
    FollowersResponse
)

router = APIRouter()

@router.get("/")
async def root():
    raise HTTPException(status_code=400, detail="Missing username parameter")

@router.get("/{username}", response_model=ProfileResponse)
async def user_info(username: str):
    return await get_user_details(username)

@router.get("/{username}/repos", response_model=RepositoriesResponse)
async def user_repos(username: str):
    return await get_user_repos(username)

@router.get("/{username}/followers", response_model=FollowersResponse)
async def user_followers(username: str):
    return await get_user_followers(username)
