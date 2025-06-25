from fastapi import APIRouter
from app.api import user, repos, search, graphql

router = APIRouter()

router.include_router(user.router, prefix="/user", tags=["user"])
router.include_router(repos.router, prefix="/repos", tags=["repos"])
router.include_router(search.router, prefix="/search", tags=["search"])
router.include_router(graphql.router, prefix="/graphql", tags=["graphql"])
