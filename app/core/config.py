from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # GithubAPI
    AUTH_TOKEN: Optional[str] = None
    GITHUB_API_URL: str = "https://api.github.com/"

    # Middleware
    ALLOW_ORIGINS: List[str] = ["*"]
    ALLOW_METHODS: List[str] = ["GET", "POST"]
    ALLOWED_HOSTS: List[str] = [
        "wrappergithubapi-production.up.railway.app",
        "localhost",
        "127.0.0.1"
    ]
    RATE_LIMIT: str = "30/minute"
    GZIP_COMPRESS_LEVEL: int = 7

    # Headers
    CSP: str = (
        "default-src 'self';"
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com;"
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net;"
        "img-src 'self' https://fastapi.tiangolo.com https://cdn.redoc.ly data:;"
        "font-src https://fonts.gstatic.com;"
        "connect-src 'self';"
        "object-src 'none';"
        "worker-src 'self' blob:;"
        "upgrade-insecure-requests;"
    )
    STRICT_TRANSPORT_SECURITY: str = "max-age=63072000; includeSubDomains; preload"
    PERMISSION_POLICY: str = "geolocation=(), microphone=(), camera=()"
    REFERRER_POLICY: str = "no-referrer"
    X_CONTENT_TYPE_OPTIONS: str = "nosniff"
    X_FRAME_OPTIONS: str = "DENY"

    # Logging
    LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
