from fastapi import APIRouter
from app.api import user, repos

router = APIRouter()

router.include_router(user.router)
router.include_router(repos.router)