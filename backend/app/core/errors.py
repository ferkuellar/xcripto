from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class NotFoundError(HTTPException):
    def __init__(self, resource: str) -> None:
        super().__init__(status_code=404, detail=f"{resource} not found")


class DomainValidationError(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=400, detail=message)


class ConflictError(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=409, detail=message)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": str(exc.detail),
            "correlation_id": getattr(request.state, "correlation_id", None),
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Request validation failed",
            "details": jsonable_encoder(exc.errors(), custom_encoder={ValueError: str}),
            "correlation_id": getattr(request.state, "correlation_id", None),
        },
    )
