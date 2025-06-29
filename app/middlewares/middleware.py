from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIASGIMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.middlewares.other_middleware import (
    ResponseTimeMiddleware, SecurityHeadersMiddleware
)
from app.core.config import settings

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])

def add_middleware(app: FastAPI):
    app.state.__setattr__("limiter", limiter)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts = settings.ALLOWED_HOSTS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins = settings.ALLOW_ORIGINS,
        allow_methods = settings.ALLOW_METHODS
    )
    app.add_middleware(SlowAPIASGIMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(ResponseTimeMiddleware)
    app.add_middleware(GZipMiddleware, compresslevel=settings.GZIP_COMPRESS_LEVEL)
