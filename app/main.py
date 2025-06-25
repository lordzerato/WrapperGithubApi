import time
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from typing import Callable, Awaitable
from app.api.routes import router
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    request_validation_exception_handler,
    general_exception_handler
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GitHub API Wrapper",
    description="This API allows users to query GitHub data using both REST and GraphQL endpoints.",
    version="1.0"
)

@app.middleware("http")
async def add_process_time_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        f'Request to "{request.method} {request.url.path}" processed in {process_time:.4f}s'
    )
    return response

@app.exception_handler(HTTPException)
async def custom_http_exception(request: Request, exc: HTTPException):
    return await http_exception_handler(request, exc)
@app.exception_handler(ValidationError)
async def custom_validation_exception(request: Request, exc: ValidationError):
    return await validation_exception_handler(request, exc)
@app.exception_handler(RequestValidationError)
async def custom_request_validation_exception(request: Request, exc: RequestValidationError):
    return await request_validation_exception_handler(request, exc)
@app.exception_handler(Exception)
async def custom_general_exception(request: Request, exc: Exception):
    return await general_exception_handler(request, exc)

app.include_router(router)
