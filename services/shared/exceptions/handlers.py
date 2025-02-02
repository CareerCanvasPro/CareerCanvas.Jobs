from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Union
from .base import JobAPIException

async def job_exception_handler(
    request: Request,
    exc: JobAPIException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )

async def validation_exception_handler(
    request: Request,
    exc: Union[ValueError, TypeError]
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": str(exc),
            "details": None
        }
    )