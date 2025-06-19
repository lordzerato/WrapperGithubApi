from fastapi import APIRouter, HTTPException
from typing import List
from app.services.github_client import get_user_details, get_user_repos, get_user_followers
from app.models.response_schema import User, Profile, Repository

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/{username}", response_model=Profile)
async def user_info(username: str):
    data = await get_user_details(username)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return Profile.model_validate(data)


@router.get("/{username}/repos", response_model=List[Repository])
async def user_repos(username: str):
    data = await get_user_repos(username)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    repos = [Repository.model_validate(repo) for repo in data]
    return repos

@router.get("/{username}/followers", response_model=List[User])
async def user_followers(username: str):
    data = await get_user_followers(username)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    followers = [User.model_validate(follower) for follower in data]
    return followers
