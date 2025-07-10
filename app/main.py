from fastapi import FastAPI
from app.api.routes import router
from app.middlewares.middleware import add_middleware
from app.core.exceptions import add_exception_handler
from app.core.lifespan import app_lifespan
import app.core.logger as logger

logger.setup_logging()

app = FastAPI(
    title="GitHub API Wrapper",
    description="This API allows users to query GitHub data using both REST and GraphQL endpoints.",
    version="1.0",
    lifespan=app_lifespan
)

add_exception_handler(app)
add_middleware(app)

app.include_router(router)
