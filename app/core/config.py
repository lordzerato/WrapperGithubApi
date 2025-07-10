import re
from typing import get_args
from pydantic import field_validator, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.models.types import Methods, PropsHeaders, RequiredCsp, Pattern, LogLevel

class Settings(BaseSettings):
    # GithubAPI
    AUTH_TOKEN: str | None = None
    GITHUB_API_URL: HttpUrl = HttpUrl("https://api.github.com/")

    # Redis
    REDIS_URL: str = ""
    # Kafka
    KAFKA_SERVER: str = ""
    # Logging
    LOGGING_LEVEL: LogLevel = "INFO"

    # Middleware
    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_METHODS: list[str] = ["GET", "POST"]
    ALLOWED_HOSTS: list[str] = [
        "wrappergithubapi-production.up.railway.app",
        "localhost",
        "127.0.0.1"
    ]
    RATE_LIMIT: str = "30/minute"
    GZIP_COMPRESS_LEVEL: int = 7

    # Headers
    headers: dict[str, str] = {
        "CSP": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
            "img-src 'self' https://fastapi.tiangolo.com https://cdn.redoc.ly data:; "
            "font-src https://fonts.gstatic.com; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "worker-src 'self' blob:; "
            "upgrade-insecure-requests;"
        ),
        "STRICT_TRANSPORT_SECURITY": "max-age=63072000; includeSubDomains",
        "PERMISSION_POLICY" : "geolocation=(), microphone=(), camera=()",
        "REFERRER_POLICY" : "no-referrer",
        "X_CONTENT_TYPE_OPTIONS" : "nosniff",
        "X_FRAME_OPTIONS": "DENY"
    }

    @field_validator("ALLOW_METHODS")
    @classmethod
    def validate_allow_methods(cls, value: list[str]) -> list[str]:
        for method in value:
            if method.upper() not in get_args(Methods):
                raise ValueError(f"Invalid method: {method}")
        return value

    @field_validator("RATE_LIMIT")
    @classmethod
    def validate_rate_limit(cls, value: str) -> str:
        if re.fullmatch(Pattern, value):
            return value
        raise ValueError("Invalid RATE_LIMIT format (expected: <number>/(minute|second|hour))")

    @field_validator("GZIP_COMPRESS_LEVEL")
    @classmethod
    def validate_gzip_compress_level(cls, value: int) -> int:
        if value < 1 or value > 9:
            raise ValueError("GZIP_COMPRESS_LEVEL must be between 1 and 9")
        return value

    @field_validator("headers")
    @classmethod
    def validate_headers(cls, value: dict[str, str]) -> dict[str, str]:
        for key, val in value.items():
            if key not in PropsHeaders:
                raise ValueError(f"Invalid header key: {key}")
            match key:
                case "CSP":
                    missing = [props for props in RequiredCsp if props not in val.split(" ")]
                    if missing:
                        raise ValueError(f"Missing required CSP properties: {', '.join(missing)}")
                case "REFERRER_POLICY":
                    if val not in ["no-referrer", "strict-origin-when-cross-origin"]:
                        raise ValueError(f"Invalid REFERRER_POLICY value: {val}")
                case "X_CONTENT_TYPE_OPTIONS":
                    if val != "nosniff":
                        raise ValueError(f"Invalid X_CONTENT_TYPE_OPTIONS value: {val}")
                case "X_FRAME_OPTIONS":
                    if val not in ["DENY", "SAMEORIGIN"]:
                        raise ValueError(f"Invalid X_FRAME_OPTIONS value: {val}")
                case _:
                    if not value:
                        raise ValueError(f"Invalid value of {key}")
        return value

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
