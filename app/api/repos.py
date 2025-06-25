from fastapi import APIRouter
from app.services.github_client import get_repo_details
from app.models.response_schema import RepositoryDetailsResponse

router = APIRouter()

@router.get("/{username}/{repository}", response_model=RepositoryDetailsResponse)
async def repo_info(username: str, repository: str):
    return await get_repo_details(username, repository)
