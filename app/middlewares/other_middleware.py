import time
from fastapi import Request
from fastapi.responses import Response
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable, Any
from app.core.kafka import producer_send
from app.core.logger import logger
from app.core.config import settings
from app.models.types import JSON

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
        client_host = request.client.host if request.client else "unknown"
        logger.info(
            f'{client_host} - "{request.method} {request.url.path}" processed in {process_time:.4f}s'
        )
        log_data: JSON = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(process_time * 1000, 2),
            "client_host": client_host,
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }
        await producer_send("api-activity-log", log_data)
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
