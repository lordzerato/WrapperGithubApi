
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.services.github_client import get_repo_details
from app.models.response_schema import RepositoryDetails

router = APIRouter(prefix="/repos", tags=["repos"])

@router.get("/{owner}/{repo}", response_model=RepositoryDetails)
async def repo_info(owner: str, repo: str):
    data = await get_repo_details(owner, repo)
    if not data:
        raise HTTPException(status_code=404, detail="Repository not found")

    try:
        data_repo = RepositoryDetails.model_validate(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return data_repo
