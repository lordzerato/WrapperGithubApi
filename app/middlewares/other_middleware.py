import time
from fastapi import Request
from fastapi.responses import Response
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable, Any
from app.core.logger import logger
from app.core.config import settings

class ResponseTimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, *args: Any, **kwargs: Any):
        super().__init__(app, *args, **kwargs)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()
        response: Response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(
            f'Request to "{request.method} {request.url.path}" processed in {process_time:.4f}s'
        )
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, *args: Any, **kwargs: Any):
        super().__init__(app, *args, **kwargs)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response: Response = await call_next(request)
        # to avoid Clickjacking, XSS, insecure redirects
        for key, value in settings.headers.items():
            response.headers[key] = value
        return response
