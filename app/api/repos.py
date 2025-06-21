
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.services.github_client import get_repo_details
from app.models.response_schema import RepositoryDetailsResponse

router = APIRouter(prefix="/repos", tags=["repos"])

@router.get("/{username}/{repository}", response_model=RepositoryDetailsResponse)
async def repo_info(username: str, repository: str):
    data = await get_repo_details(username, repository)
    if not data:
        raise HTTPException(status_code=404, detail="Repository not found")

    try:
        data_repo = RepositoryDetailsResponse.model_validate(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return data_repo
