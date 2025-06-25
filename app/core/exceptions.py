import logging
from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.models.errors import GithubErrorRequest, FormattedErrorRequest
from typing import List

logger = logging.getLogger(__name__)

def reformat_error(
    exc: ValidationError | RequestValidationError, isValidation: bool = False
) -> List[FormattedErrorRequest]:
    errors: List[GithubErrorRequest] = [
        GithubErrorRequest.model_validate(error) for error in exc.errors()
    ]
    formatted_errors: List[FormattedErrorRequest] = []

    for error in errors:
        default_loc = ("Unknown error") if isValidation else ["", "Unknown error"]
        loc = error.loc or default_loc
        invalid_value = error.input["message"] if isinstance(error.input, dict) else error.input
        formatted_error: FormattedErrorRequest = FormattedErrorRequest.model_validate(
            {
                "field": loc[0] if isValidation else loc[1],
                "message": error.msg or "Unknown error",
                "error_type": error.type or "Unknown",
                "invalid_value": invalid_value
            }
        )
        formatted_errors.append(formatted_error)

    return formatted_errors
    

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

async def validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    formatted_errors = reformat_error(exc, True)
    return JSONResponse(
        status_code=422, content={"detail": jsonable_encoder(formatted_errors)}
    )

async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    formatted_errors = reformat_error(exc)
    return JSONResponse(
        status_code=422, content={"detail": jsonable_encoder(formatted_errors)}
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        f"Unhandled exception for {request.method} {request.url.path}: {exc}",
        exc_info=True
    )

    status = getattr(exc, "status", getattr(exc, "status_code", 500))
    return JSONResponse(
        status_code=status, content={"detail": f"Internal Server Error: {str(exc)}"}
    )
