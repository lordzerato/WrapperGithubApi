from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from slowapi.errors import RateLimitExceeded
from app.models.error import RawErrorValidation, FormattedErrorValidation
from app.core.logger import logger

def reformat_error(
    exc: ValidationError | RequestValidationError, isValidation: bool = False
) -> list[FormattedErrorValidation]:
    errors: list[RawErrorValidation] = [
        RawErrorValidation.model_validate(error) for error in exc.errors()
    ]
    formatted_errors: list[FormattedErrorValidation] = []

    for error in errors:
        loc = list(error.loc or ("Unknown error", ""))[::1 if isValidation else -1]
        indexLoc = 1 if isinstance(loc[0], int) else 0
        invalid_value = error.input.get("message") if isinstance(error.input, dict) else error.input
        formatted_error: FormattedErrorValidation = FormattedErrorValidation.model_validate(
            {
                "field": loc[indexLoc],
                "message": error.msg or "Unknown error",
                "error_type": error.type or "Unknown",
                "invalid_value": invalid_value
            }
        )
        formatted_errors.append(formatted_error)

    return formatted_errors

def add_exception_handler(app: FastAPI):
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exception_handler(
        request: Request, exc: RateLimitExceeded
    ) -> JSONResponse:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded, please try again later."}
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        formatted_errors = reformat_error(exc, True)
        return JSONResponse(
            status_code=422, content={"detail": jsonable_encoder(formatted_errors)}
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        formatted_errors = reformat_error(exc)
        return JSONResponse(
            status_code=422, content={"detail": jsonable_encoder(formatted_errors)}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error(
            f"Unhandled exception for {request.method} {request.url.path}: {exc}",
            exc_info=True
        )

        status = getattr(exc, "status", getattr(exc, "status_code", 500))
        return JSONResponse(
            status_code=status, content={"detail": f"Internal Server Error: {str(exc)}"}
        )
