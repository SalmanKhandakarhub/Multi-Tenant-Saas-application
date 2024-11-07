from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"{exc.status_code}: {exc.detail}"}
    )

async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = []

    for error in errors:
        field = ".".join([str(loc) for loc in error['loc']])
        message = error['msg']
        formatted_errors.append(f"{message} at {field}")

    error_message = "; ".join(formatted_errors)
    return JSONResponse(
        status_code=422, 
        content={"message": f"422: {error_message}"}
    )
