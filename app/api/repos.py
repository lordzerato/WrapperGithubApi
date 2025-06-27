from fastapi import APIRouter, HTTPException
from app.services.github_client import get_repo_details
from app.models.response_schema import RepositoryDetailsResponse

router = APIRouter(prefix="/repos", tags=["repos"])

@router.get("/", include_in_schema=False)
async def root():
    raise HTTPException(400, "Missing username parameter")

@router.get("/{username}", include_in_schema=False)
async def root_username():
    raise HTTPException(400, "Missing repository parameter")

@router.get("//{repository}", include_in_schema=False)
async def root_repository():
    raise HTTPException(400, "Missing username parameter")

@router.get("/{username}/{repository}", response_model=RepositoryDetailsResponse)
async def repo_info(username: str, repository: str):
    return await get_repo_details(username, repository)
