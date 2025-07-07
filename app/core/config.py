import re
from typing import Literal
from pydantic import field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

pattern = r"^(?!0)\d+/(second|minute|hour|day|month|year)$"
type_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
props_headers: list[str] = ["CSP", "STRICT_TRANSPORT_SECURITY", "PERMISSION_POLICY", "REFERRER_POLICY", "X_CONTENT_TYPE_OPTIONS", "X_FRAME_OPTIONS"]
required_csp: list[str] = ["default-src", "script-src", "style-src", "img-src", "font-src", "worker-src", "connect-src"]

class Settings(BaseSettings):
    # GithubAPI
    AUTH_TOKEN: str | None = None
    GITHUB_API_URL: AnyHttpUrl = AnyHttpUrl("https://api.github.com/")

    # Redis
    REDIS_URL: str = ""

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

    # Logging
    LOGGING_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @field_validator("ALLOW_METHODS")
    @classmethod
    def validate_allow_methods(cls, value: list[str]) -> list[str]:
        for method in value:
            if method not in type_methods:
                raise ValueError(f"Invalid method: {method}")
        return value

    @field_validator("RATE_LIMIT")
    @classmethod
    def validate_rate_limit(cls, value: str) -> str:
        if re.fullmatch(pattern, value):
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
            if key not in props_headers:
                raise ValueError(f"Invalid header key: {key}")
            match key:
                case "CSP":
                    missing = [props for props in required_csp if props not in val.split(" ")]
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
