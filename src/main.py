from xml.etree.ElementInclude import include, XINCLUDE_INCLUDE

from fastapi import FastAPI, requests, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from api.master_api import router as master_api
from api.tenant_api import router as tenant_api
from core.config import settings
from middlewares import TenantMiddleware
from utils.exceptions import custom_http_exception_handler, custom_validation_exception_handler


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json"
)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_origins=[
        #     str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        # ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(TenantMiddleware)


# Custom exception handlers
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)


app.include_router(master_api, prefix="/master", include_in_schema=True)
app.include_router(tenant_api, prefix="/tenant", include_in_schema=True)

