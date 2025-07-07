from fastapi import APIRouter, HTTPException
from typing import Literal
from app.services.github_client.users import (
    get_user_details,
    get_user_repos,
    get_user_followers,
    get_user_starred,
    get_user_public_event
)
from app.models.response_schema import (
    UsersDetailsResponse,
    UsersRepositoriesResponse,
    UsersFollowersResponse,
    UsersStarredResponse,
    UsersPublicEventsResponse
)
from app.utils.utils import join_query_params

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/", include_in_schema=False)
async def root():
    raise HTTPException(status_code=400, detail="Missing username parameter")

@router.get("s/", include_in_schema=False)
async def root_users():
    raise HTTPException(status_code=400, detail="Missing username parameter")

@router.get("s/{username}", response_model=UsersDetailsResponse)
async def user_info(username: str):
    return await get_user_details(f"{username}")

@router.get("s/{username}/repos", response_model=UsersRepositoriesResponse)
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
    return await get_user_repos(f"{username}/repos", query_params)

@router.get("s/{username}/followers", response_model=UsersFollowersResponse)
async def user_followers(username: str, page: int = 1, per_page: int = 30):
    query_params: str = join_query_params({"page": page, "per_page": per_page})
    return await get_user_followers(f"{username}/followers", query_params)

@router.get("s/{username}/starred", response_model=UsersStarredResponse)
async def user_starred(username: str, page: int = 1, per_page: int = 30):
    query_params: str = join_query_params({"page": page, "per_page": per_page})
    return await get_user_starred(f"{username}/starred", query_params)

@router.get("s/{username}/events/public", response_model=UsersPublicEventsResponse)
async def user_public_event(username: str, page: int = 1, per_page: int = 30):
    query_params: str = join_query_params({"page": page, "per_page": per_page})
    return await get_user_public_event(f"{username}/events/public", query_params)
