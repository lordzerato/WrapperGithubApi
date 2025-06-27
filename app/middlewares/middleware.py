from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIASGIMiddleware
from app.middlewares.other_middleware import (
    ResponseTimeMiddleware, CustomHTTPSRedirectMiddleware
)

limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])

def add_middleware(app: FastAPI):
    app.state.__setattr__("limiter", limiter)
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"]
    )
    app.add_middleware(SlowAPIASGIMiddleware)
    app.add_middleware(CustomHTTPSRedirectMiddleware)
    app.add_middleware(GZipMiddleware, compresslevel=7)
    app.add_middleware(ResponseTimeMiddleware)
