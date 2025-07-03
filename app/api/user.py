from fastapi import APIRouter, HTTPException
from typing import Literal
from app.services.github_client import (
    get_user_details,
    get_user_repos,
    get_user_followers
)
from app.models.response_schema import (
    ProfileResponse,
    UsersRepositoriesResponse,
    FollowersResponse
)
from app.utils.utils import join_query_params

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/", include_in_schema=False)
async def root():
    raise HTTPException(status_code=400, detail="Missing username parameter")

@router.get("/{username}", response_model=ProfileResponse)
async def user_info(username: str):
    return await get_user_details(username)

@router.get("/{username}/repos", response_model=UsersRepositoriesResponse)
async def user_repos(
    username: str,
    type: Literal["all", "owner", "member"] = "owner",
    sort: Literal["created", "updated", "pushed", "full_name"] = "full_name",
    direction: Literal["asc", "desc"] = "asc",
    page: int = 1,
    per_page: int = 30
):
    query_params: str = join_query_params({
        "type": type,
        "sort": sort,
        "direction": direction,
        "page": page,
        "per_page": per_page
    })
    print(query_params)
    return await get_user_repos(username, query_params)

@router.get("/{username}/followers", response_model=FollowersResponse)
async def user_followers(username: str, page: int = 1, per_page: int = 30):
    query_params: str = join_query_params({"page": page, "per_page": per_page})
    return await get_user_followers(username, query_params)
