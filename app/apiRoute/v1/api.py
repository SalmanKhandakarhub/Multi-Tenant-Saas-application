from fastapi import APIRouter
from app.apiRoute.v1.endpoints import auth, users, tenants
# from ...apiRoute.v1.endpoints import auth, users, tenants

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])