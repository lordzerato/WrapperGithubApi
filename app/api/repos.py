
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.services.github_client import get_repo_details
from app.models.response_schema import RepositoryDetailsResponse

router = APIRouter(prefix="/repos", tags=["repos"])

@router.get("/{username}/{repository}", response_model=RepositoryDetailsResponse)
async def repo_info(username: str, repository: str):
    try:
        data = await get_repo_details(username, repository)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        status = getattr(e, "status", 500)
        raise HTTPException(status_code=status, detail=str(e))

    return data
