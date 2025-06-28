import time
from fastapi import Request
from fastapi.responses import Response
from starlette.types import ASGIApp
# from starlette.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable, Any
from app.core.logger import logger

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

class CustomHTTPSRedirectMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, *args: Any, **kwargs: Any):
        super().__init__(app, *args, **kwargs)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        client_host = request.client.host if request.client else None
        
        if client_host == "127.0.0.1" or client_host == "localhost":
            response = await call_next(request)
        else:
            if request.url.scheme != "https":
                # return RedirectResponse(url=request.url.replace(scheme="https"))
            response = await call_next(request)
        
        return response
