from fastapi import APIRouter, HTTPException
from typing import List
from app.services.github_client import get_user_details, get_user_repos, get_user_followers
from app.models.response_schema import ProfileResponse, RepositoryResponse, FollowersResponse

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/{username}", response_model=ProfileResponse)
async def user_info(username: str):
    data = await get_user_details(username)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    profile = ProfileResponse.model_validate(data)
    return profile


@router.get("/{username}/repos", response_model=List[RepositoryResponse])
async def user_repos(username: str):
    data = await get_user_repos(username)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    repos = [RepositoryResponse.model_validate(repo) for repo in data]
    return repos

@router.get("/{username}/followers", response_model=FollowersResponse)
async def user_followers(username: str):
    data = await get_user_followers(username)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    followers = FollowersResponse.model_validate(data)
    return followers
