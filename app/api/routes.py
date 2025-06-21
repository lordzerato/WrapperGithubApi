from fastapi import APIRouter
from app.api import user, repos, search

router = APIRouter()

router.include_router(user.router)
router.include_router(repos.router)
router.include_router(search.router)
