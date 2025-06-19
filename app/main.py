from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="GitHub API Wrapper",
    version="1.0"
)

app.include_router(router)
